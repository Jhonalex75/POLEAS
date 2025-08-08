
from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64

app = Flask(__name__)

# Datos de la tabla de poleas (para 4 canales)
poleas_estandares = {
    4: [7.35, 7.75, 8.35, 8.95, 9.75, 11.35, 12.75]  # Diámetros en pulgadas
}

# Tabla de capacidad para correas 5V (valores del manual Intermec)
tabla_capacidad_5V = {
    1000: 14.0,
    1200: 16.5,
    1400: 19.0,
    1600: 21.5,
    1750: 23.5,
    1800: 24.2,  # Valor para 1800 RPM
    2000: 26.5
}

# Curva de la bomba (datos del manual)
curva_base = {
    'rpm': 2020,
    'q': 88,    # m³/hr
    'h': 43.8   # metros
}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calcular', methods=['POST'])
def calcular():
    rpm_motor = float(request.form['rpm_motor'])
    hp_motor = float(request.form['hp_motor'])
    rpm_bomba = float(request.form['rpm_bomba'])
    centro_dist = float(request.form['centro_dist'])
    diam_motor = float(request.form['diam_motor'])
    canales_motor = int(request.form['canales_motor'])

    factor_servicio = 1.6
    hp_diseno = hp_motor * factor_servicio
    relacion_velocidad = rpm_motor / rpm_bomba
    diam_bomba = diam_motor * relacion_velocidad
    diam_bomba = round(diam_bomba, 2)
    std_diam = min(poleas_estandares[canales_motor], key=lambda x: abs(x - diam_bomba))
    diam_bomba_std = std_diam if abs(std_diam - diam_bomba) < 1 else diam_bomba
    rpm_ordenadas = sorted(tabla_capacidad_5V.keys())
    for i in range(len(rpm_ordenadas)-1):
        if rpm_ordenadas[i] <= rpm_motor <= rpm_ordenadas[i+1]:
            rpm1 = rpm_ordenadas[i]
            rpm2 = rpm_ordenadas[i+1]
            cap1 = tabla_capacidad_5V[rpm1]
            cap2 = tabla_capacidad_5V[rpm2]
            capacidad_por_canal = cap1 + (cap2 - cap1) * (rpm_motor - rpm1)/(rpm2 - rpm1)
            break
    else:
        capacidad_por_canal = tabla_capacidad_5V[min(rpm_ordenadas, key=lambda x: abs(x-rpm_motor))]
    capacidad_total = capacidad_por_canal * canales_motor
    factor_seguridad = round(capacidad_total / hp_diseno, 2)
    C = centro_dist / 25.4
    D = diam_motor
    d = diam_bomba_std
    L = 2*C + (np.pi/2)*(D + d) + ((D - d)**2)/(4*C)
    L = round(L, 2)
    plot_url = generar_grafica(rpm_bomba, rpm_motor)
    return render_template('index.html',
        diam_bomba=diam_bomba_std,
        canales_bomba=canales_motor,
        tipo_correa='5V',
        longitud=L,
        factor_seguridad=factor_seguridad,
        capacidad_total=round(capacidad_total, 1),
        hp_diseno=round(hp_diseno, 1),
        plot_url=plot_url
    )

def generar_grafica(rpm_operacion, rpm_motor):
    # --- 1. Generar una curva base realista ---
    q_base = curva_base['q']
    h_base = curva_base['h']
    rpm_base = curva_base['rpm']
    
    q_max_base = q_base * 1.8
    h_max_base = h_base / (1 - (q_base**2 / q_max_base**2)) if (1 - (q_base**2 / q_max_base**2)) != 0 else h_base * 1.2
    k_base = h_max_base / (q_max_base**2)

    q_range_base = np.linspace(0, q_max_base, 100)
    h_range_base = h_max_base - k_base * q_range_base**2

    # --- 2. Aplicar Leyes de Afinidad para escalar la curva ---
    def escalar_curva(rpm_nueva):
        factor_q = rpm_nueva / rpm_base
        factor_h = (rpm_nueva / rpm_base)**2
        q_nueva = q_range_base * factor_q
        h_nueva = h_range_base * factor_h
        return q_nueva, h_nueva

    q_2000, h_2000 = escalar_curva(2000)
    q_1600, h_1600 = escalar_curva(1600)
    q_operacion, h_operacion = escalar_curva(rpm_operacion)

    # --- 3. Calcular el punto de operación actual ---
    q_op_actual = q_base * (rpm_operacion / rpm_base)
    h_op_actual = h_base * (rpm_operacion / rpm_base)**2

    # --- 4. Crear la gráfica con Matplotlib ---
    plt.figure(figsize=(10, 6))
    plt.plot(q_2000, h_2000, 'b-', label='Curva a 2000 RPM', linewidth=2)
    plt.plot(q_1600, h_1600, 'r-', label='Curva a 1600 RPM', linewidth=2)
    plt.plot(q_operacion, h_operacion, 'g--', label=f'Curva a {rpm_operacion:.0f} RPM (Actual)', linewidth=2)
    
    plt.scatter(q_op_actual, h_op_actual, color='green', s=120, zorder=5, label=f'Punto de Operación Actual ({q_op_actual:.1f} m³/hr, {h_op_actual:.1f} m)')
    
    plt.title('Curvas de Rendimiento de la Bomba', fontsize=16)
    plt.xlabel('Caudal (m³/hr)', fontsize=12)
    plt.ylabel('Altura (m)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(fontsize=10)
    plt.xlim(left=0)
    plt.ylim(bottom=0)
    plt.tight_layout()

    # --- 5. Convertir la gráfica a imagen base64 ---
    img_buf = BytesIO()
    plt.savefig(img_buf, format='png', dpi=100)
    img_buf.seek(0)
    img_data = base64.b64encode(img_buf.read()).decode('utf-8')
    plt.close()
    
    return f"data:image/png;base64,{img_data}"

if __name__ == '__main__':
    app.run(debug=True)