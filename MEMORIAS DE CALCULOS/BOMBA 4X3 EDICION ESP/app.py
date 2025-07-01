# -----------------------------------------------------------------------------
# Aplicación Flask para Diseño de Transmisión por Polea y Correa
# Basado en los conceptos del libro "Diseño de Elementos de Máquinas" de Mott
# Ver catalogo Interme.
# y el manual de la bomba Warman WPA43A03.
#
# Para ejecutar esta aplicación:
# 1. Asegúrate de tener Python instalado.
# 2. Instala las librerías necesarias:
#    pip install Flask matplotlib
# 3. Guarda este código como "app.py".
# 4. Ejecuta desde la terminal: python app.py
# 5. Abre tu navegador web y ve a http://127.0.0.1:5000
# -----------------------------------------------------------------------------

import math
import io
import base64
from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import numpy as np

# Inicializar la aplicación Flask
app = Flask(__name__)

# --- Funciones de Cálculo de Ingeniería ---

def calcular_diseno_correa(potencia_hp, rpm_motor, rpm_bomba, d_motora, C_mm):
    """
    Realiza los cálculos de diseño para la transmisión por correa en V.
    """
    resultados = {}

    # --- 1. Conversión de Unidades y Datos Iniciales ---
    C = C_mm / 25.4  # Convertir distancia entre centros de mm a pulgadas
    resultados['C_in'] = C

    # --- 2. Diámetro de la Polea Conducida (Bomba) ---
    d_bomba = (rpm_motor / rpm_bomba) * d_motora
    resultados['d_bomba'] = d_bomba

    # --- 3. Longitud de la Correa (Fórmula de Mott, Cap. 7) ---
    # L ≈ 2C + 1.57(D₂ + D₁) + (D₂ - D₁)² / 4C
    L = 2 * C + 1.57 * (d_bomba + d_motora) + (d_bomba - d_motora)**2 / (4 * C)
    
    # Seleccionar longitud de correa estándar (basado en catálogos típicos)
    # Para correas 5V, longitudes comunes son 90, 95, 100, 106, 112, etc.
    longitudes_std_5v = [90, 95, 100, 106, 112, 118, 125, 132, 140, 150]
    longitud_seleccionada = min(longitudes_std_5v, key=lambda x: abs(x - L))
    resultados['longitud_correa'] = longitud_seleccionada

    # --- 4. Distancia entre Centros Real ---
    # Recalcular C con la longitud estándar (Fórmula de Mott, Cap. 7)
    B = 4 * longitud_seleccionada - 6.28 * (d_bomba + d_motora)
    # Se agrega manejo de error en caso de que el valor dentro de sqrt sea negativo
    try:
        C_real = (B + math.sqrt(B**2 - 32 * (d_bomba - d_motora)**2)) / 16
    except ValueError:
        C_real = C # Si hay un error, se mantiene la C original
    resultados['C_real'] = C_real

    # --- 5. Ángulo de Contacto (Fórmula de Mott, Cap. 7) ---
    # θ₁ = 180° - 2 * arcsin((D₂ - D₁) / 2C)
    try:
        theta_rad = math.pi - 2 * math.asin((d_bomba - d_motora) / (2 * C_real))
        theta_deg = math.degrees(theta_rad)
    except ValueError:
        theta_deg = 180.0 # Ocurre si D1 > D2
    resultados['angulo_contacto'] = theta_deg

    # --- 6. Cálculo de Potencia de Diseño y Número de Correas ---
    # Factor de servicio (Tabla 7-1, Mott) para Bomba Centrífuga, >15h/día
    # Motor CA par normal (1.2), Motor de combustión (1.4). Usamos un intermedio
    # conservador para una bomba de lodos.
    factor_servicio = 1.4
    potencia_diseno = potencia_hp * factor_servicio
    resultados['potencia_diseno'] = potencia_diseno

    # Potencia nominal por correa 5V (Datos de ejemplo basados en tablas de fabricantes)
    # Para d_motora = 8.95" @ 1800 rpm
    potencia_base_correa = 28.5  # HP, valor típico de tablas
    # Potencia adicional por relación de velocidad
    relacion_velocidad = rpm_motor / rpm_bomba
    potencia_adicional = 0.85 # HP, para VR ~ 1.125
    potencia_nominal_correa = potencia_base_correa + potencia_adicional

    # Factores de corrección
    # Factor de corrección por ángulo de contacto (C_theta) - (Fig. 7-14 Mott)
    if theta_deg > 175: C_theta = 1.0
    elif theta_deg > 165: C_theta = 0.98
    elif theta_deg > 154: C_theta = 0.95
    elif theta_deg > 140: C_theta = 0.92
    else: C_theta = 0.88
    
    # Factor de corrección por longitud (C_L) - (Fig. 7-15 Mott)
    if longitud_seleccionada > 132: C_L = 1.05
    elif longitud_seleccionada > 106: C_L = 1.0
    else: C_L = 0.95

    potencia_corregida_correa = potencia_nominal_correa * C_theta * C_L
    resultados['potencia_corregida'] = potencia_corregida_correa

    # Número de correas
    num_correas_calculado = potencia_diseno / potencia_corregida_correa
    num_correas_seleccionado = math.ceil(num_correas_calculado)
    resultados['num_correas'] = num_correas_seleccionado

    # --- 7. Factor de Seguridad ---
    # Relación entre la capacidad total instalada y la potencia de diseño
    capacidad_total = num_correas_seleccionado * potencia_corregida_correa
    factor_seguridad = capacidad_total / potencia_diseno
    resultados['factor_seguridad'] = factor_seguridad

    return resultados

def generar_grafico_bomba():
    """
    Genera el gráfico de las curvas de la bomba y la resistencia del sistema.
    Los datos se extraen visualmente del PDF "WPA43A03_RZ_4X3...".
    """
    # Datos extraídos del PDF para la bomba Warman 4/3 AH
    # Curva a 1600 RPM
    flujo_1600 = np.array([0, 50, 100, 150, 200])
    cabeza_1600 = np.array([31, 29, 25, 18, 8])

    # Curva a 2000 RPM
    flujo_2000 = np.array([0, 50, 100, 150, 200, 250])
    cabeza_2000 = np.array([51, 49, 45, 38, 29, 18])

    # Cálculo de la curva de resistencia del sistema
    # Basado en el punto de operación de referencia: Q=88 m³/h, H=43.8 m @ 2020 RPM
    # Usamos las leyes de afinidad para escalar el punto a 1600 RPM
    Q_ref = 88.0
    H_ref = 43.8
    n_ref = 2020.0
    n_op = 1600.0

    # Punto de operación escalado
    Q_op = Q_ref * (n_op / n_ref)
    H_op = H_ref * (n_op / n_ref)**2
    
    # La curva del sistema es H = k * Q²
    k = H_op / (Q_op**2)
    
    flujo_sistema = np.linspace(0, 200, 100)
    cabeza_sistema = k * flujo_sistema**2

    # Creación del gráfico
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(flujo_1600, cabeza_1600, 'b-', label='Curva Bomba @ 1600 RPM', lw=2)
    ax.plot(flujo_2000, cabeza_2000, 'g--', label='Curva Bomba @ 2000 RPM', lw=2)
    ax.plot(flujo_sistema, cabeza_sistema, 'r:', label='Curva Resistencia del Sistema', lw=2)
    
    # Marcar el punto de operación
    ax.plot(Q_op, H_op, 'ko', markersize=8, label=f'Punto de Operación ({Q_op:.1f} m³/h, {H_op:.1f} m)')
    
    ax.set_title('Curvas de Rendimiento de la Bomba y del Sistema', fontsize=16)
    ax.set_xlabel('Caudal (m³/h)', fontsize=12)
    ax.set_ylabel('Altura Dinámica Total (m)', fontsize=12)
    ax.legend(fontsize=10)
    ax.set_xlim(0, 250)
    ax.set_ylim(0, 60)

    # Convertir gráfico a imagen para mostrar en la web
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plot_data = base64.b64encode(buf.read()).decode('ascii')
    plt.close(fig)
    
    return plot_data

# --- Rutas de la Aplicación ---

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Obtener datos del formulario
        potencia_hp = float(request.form.get('potencia_hp'))
        rpm_motor = float(request.form.get('rpm_motor'))
        rpm_bomba = float(request.form.get('rpm_bomba'))
        d_motora = float(request.form.get('d_motora'))
        C_mm = float(request.form.get('C_mm'))

        # Realizar cálculos
        resultados = calcular_diseno_correa(potencia_hp, rpm_motor, rpm_bomba, d_motora, C_mm)
        plot_url = generar_grafico_bomba()
        
        return render_template('index.html', 
                               resultados=resultados, 
                               plot_url=plot_url, 
                               form_data=request.form)

    # Método GET: Mostrar el formulario inicial
    # Datos por defecto según la solicitud del usuario
    default_data = {
        'potencia_hp': 75.0,
        'rpm_motor': 1800.0,
        'rpm_bomba': 1600.0,
        'd_motora': 8.95,
        'C_mm': 620.0
    }
    return render_template('index.html', resultados=None, plot_url=None, form_data=default_data)

# --- Plantilla HTML (embebida para simplicidad) ---
# En un proyecto más grande, esto estaría en un archivo separado `templates/index.html`

html_template = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Calculadora de Transmisión por Polea y Correa</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { font-family: 'Inter', sans-serif; }
    </style>
</head>
<body class="bg-gray-100 text-gray-800 p-4 md:p-8">
    <div class="max-w-6xl mx-auto bg-white rounded-2xl shadow-lg p-6 md:p-8">
        
        <header class="text-center mb-8">
            <h1 class="text-3xl md:text-4xl font-bold text-blue-700">Calculadora de Diseño de Transmisión por Polea</h1>
            <p class="text-gray-600 mt-2">Basado en conceptos de diseño de elementos de máquinas y datos de la bomba Warman.</p>
        </header>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            
            <!-- Columna de Entrada de Datos -->
            <div class="bg-gray-50 p-6 rounded-xl border border-gray-200">
                <h2 class="text-2xl font-semibold mb-6 text-blue-600 border-b pb-2">Datos de Entrada</h2>
                <form action="/" method="post">
                    <div class="space-y-4">
                        <div>
                            <label for="potencia_hp" class="block text-sm font-medium text-gray-700">Potencia del Motor (HP)</label>
                            <input type="number" step="0.1" name="potencia_hp" id="potencia_hp" value="{{ form_data.potencia_hp }}" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2">
                        </div>
                        <div>
                            <label for="rpm_motor" class="block text-sm font-medium text-gray-700">RPM del Motor</label>
                            <input type="number" step="1" name="rpm_motor" id="rpm_motor" value="{{ form_data.rpm_motor }}" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2">
                        </div>
                        <div>
                            <label for="rpm_bomba" class="block text-sm font-medium text-gray-700">RPM deseadas de la Bomba</label>
                            <input type="number" step="1" name="rpm_bomba" id="rpm_bomba" value="{{ form_data.rpm_bomba }}" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2">
                        </div>
                        <div>
                            <label for="d_motora" class="block text-sm font-medium text-gray-700">Diámetro Polea Motora (pulgadas)</label>
                            <input type="number" step="0.01" name="d_motora" id="d_motora" value="{{ form_data.d_motora }}" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2">
                        </div>
                         <div>
                            <label for="C_mm" class="block text-sm font-medium text-gray-700">Distancia entre Centros (mm)</label>
                            <input type="number" step="1" name="C_mm" id="C_mm" value="{{ form_data.C_mm }}" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm p-2">
                        </div>
                    </div>
                    <button type="submit" class="mt-6 w-full bg-blue-600 text-white font-bold py-3 px-4 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors">
                        Calcular Diseño
                    </button>
                </form>
            </div>

            <!-- Columna de Resultados -->
            <div class="bg-gray-50 p-6 rounded-xl border border-gray-200">
                <h2 class="text-2xl font-semibold mb-6 text-green-600 border-b pb-2">Resultados del Diseño</h2>
                {% if resultados %}
                <div class="space-y-3 text-gray-700">
                    <p><strong>Diámetro calculado de Polea de Bomba:</strong> <span class="font-mono text-lg text-green-700">{{ "%.2f"|format(resultados.d_bomba) }} pulgadas</span></p>
                    <p><strong>Tipo de Correa:</strong> <span class="font-mono text-lg text-green-700">5V (basado en potencia)</span></p>
                    <p><strong>Número de Canales (Correas) Requerido:</strong> <span class="font-mono text-lg text-green-700">{{ resultados.num_correas }}</span></p>
                    <p><strong>Longitud de Correa Comercial:</strong> <span class="font-mono text-lg text-green-700">{{ resultados.longitud_correa }} pulgadas</span></p>
                    <p><strong>Distancia entre Centros Real:</strong> <span class="font-mono text-lg text-green-700">{{ "%.2f"|format(resultados.C_real) }} pulgadas</span></p>
                    <p><strong>Ángulo de Contacto (Polea Menor):</strong> <span class="font-mono text-lg text-green-700">{{ "%.1f"|format(resultados.angulo_contacto) }}°</span></p>
                    <p><strong>Factor de Seguridad del Diseño:</strong> <span class="font-mono text-lg text-green-700">{{ "%.2f"|format(resultados.factor_seguridad) }}</span></p>
                </div>
                {% else %}
                <p class="text-gray-500 italic">Los resultados aparecerán aquí después de realizar el cálculo.</p>
                {% endif %}
            </div>

        </div>

        <!-- Sección de Gráfico -->
        {% if plot_url %}
        <div class="mt-8 bg-gray-50 p-6 rounded-xl border border-gray-200">
            <h2 class="text-2xl font-semibold mb-4 text-purple-600 text-center">Gráfico de Curvas de la Bomba</h2>
            <div class="flex justify-center">
                <img src="data:image/png;base64,{{ plot_url }}" alt="Gráfico de las curvas de la bomba">
            </div>
        </div>
        {% endif %}

    </div>
</body>
</html>
"""

# --- Bloque para renderizar la plantilla HTML sin necesidad de un archivo externo ---
_original_render_template = render_template
def custom_render_template(template_name, **context):
    if template_name == 'index.html':
        return app.jinja_env.from_string(html_template).render(**context)
    return _original_render_template(template_name, **context)
app.jinja_env.globals['render_template'] = custom_render_template


# Punto de entrada para ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)