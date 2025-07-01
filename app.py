
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
    # Datos de entrada
    rpm_motor = float(request.form['rpm_motor'])
    hp_motor = float(request.form['hp_motor'])
    rpm_bomba = float(request.form['rpm_bomba'])
    centro_dist = float(request.form['centro_dist'])
    diam_motor = float(request.form['diam_motor'])
    canales_motor = int(request.form['canales_motor'])
    
    # 1. Factor de servicio para bombas (según manual)
    factor_servicio = 1.6
    
    # 2. Potencia de diseño
    hp_diseno = hp_motor * factor_servicio
    
    # 3. Diámetro polea conducida (bomba)
    relacion_velocidad = rpm_motor / rpm_bomba
    diam_bomba = diam_motor * relacion_velocidad
    diam_bomba = round(diam_bomba, 2)
    
    # 4. Verificar estándar
    std_diam = min(poleas_estandares[canales_motor], 
                   key=lambda x: abs(x - diam_bomba))
    diam_bomba_std = std_diam if abs(std_diam - diam_bomba) < 1 else diam_bomba
    
    # 5. Calcular capacidad de la correa
    # Interpolación para RPM del motor
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
        capacidad_por_canal = tabla_capacidad_5V[min(rpm_ordenadas, 
                                                    key=lambda x: abs(x-rpm_motor))]
    
    # 6. Factor de seguridad
    capacidad_total = capacidad_por_canal * canales_motor
    factor_seguridad = round(capacidad_total / hp_diseno, 2)
    
    # 7. Longitud de correa
    C = centro_dist / 25.4  # mm a pulgadas
    D = diam_motor
    d = diam_bomba_std
    L = 2*C + (np.pi/2)*(D + d) + ((D - d)**2)/(4*C)
    L = round(L, 2)
    
    # Generar gráfica
    plot_url = generar_grafica(rpm_bomba, rpm_motor)
    
    return {
        'diam_bomba': diam_bomba_std,
        'canales_bomba': canales_motor,
        'tipo_correa': '5V',
        'longitud': L,
        'factor_seguridad': factor_seguridad,
        'capacidad_total': round(capacidad_total, 1),
        'hp_diseno': round(hp_diseno, 1),
        'plot_url': plot_url
    }

def generar_grafica(rpm_operacion, rpm_motor):
    # Datos de la curva base (2020 RPM)
    q_base = curva_base['q']
    h_base = curva_base['h']
    rpm_base = curva_base['rpm']
    
    # Generar puntos para la curva
    q_range = np.linspace(0, 350, 100)
    
    # Ley de afinidad para RPM
    h_2000 = h_base * (2000/rpm_base)**2 * (q_range/q_base)**2
    h_1600 = h_base * (1600/rpm_base)**2 * (q_range/q_base)**2
    h_operacion = h_base * (rpm_operacion/rpm_base)**2 * (q_range/q_base)**2
    
    # Crear figura
    plt.figure(figsize=(12, 7))
    
    # Graficar curvas para diferentes RPM
    plt.plot(q_range, h_2000, 'b-', label=f'2000 RPM', linewidth=2)
    plt.plot(q_range, h_1600, 'r-', label=f'1600 RPM (Operación)', linewidth=2)
    plt.plot(q_range, h_operacion, 'g--', label=f'{rpm_operacion} RPM (Actual)', linewidth=2)
    
    # Punto de operación
    q_op = q_base * (rpm_operacion/2020)
    h_op = h_base * (rpm_operacion/2020)**2
    plt.scatter(q_op, h_op, color='green', s=100, label='Punto operación actual')
    
    # Formato de la gráfica
    plt.title('Curvas de la Bomba - Análisis de Rendimiento', fontsize=16)
    plt.xlabel('Caudal (m³/hr)', fontsize=12)
    plt.ylabel('Altura (m)', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(fontsize=10)
    
    # Añadir anotaciones
    plt.annotate(f'RPM Motor: {rpm_motor}', xy=(10, 10), xycoords='axes pixels', fontsize=10)
    plt.annotate(f'RPM Bomba: {rpm_operacion}', xy=(10, 30), xycoords='axes pixels', fontsize=10)
    plt.annotate(f'Caudal: {q_op:.1f} m³/hr', xy=(10, 50), xycoords='axes pixels', fontsize=10)
    plt.annotate(f'Altura: {h_op:.1f} m', xy=(10, 70), xycoords='axes pixels', fontsize=10)
    
    plt.tight_layout()
    
    # Convertir a base64
    img_buf = BytesIO()
    plt.savefig(img_buf, format='png', dpi=100, bbox_inches='tight')
    img_buf.seek(0)
    img_data = base64.b64encode(img_buf.read()).decode('utf-8')
    plt.close()
    
    return f"data:image/png;base64,{img_data}"

if __name__ == '__main__':
    app.run(debug=True)