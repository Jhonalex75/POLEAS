# Calculadora de Diseño de Transmisión por Polea y Correa

Esta aplicación web, desarrollada en Python con Flask, permite calcular y visualizar el diseño de una transmisión por polea y correa en sistemas de bombeo industrial, tomando como referencia el libro "Diseño de Elementos de Máquinas" de Mott y datos reales de la bomba Warman WPA43A03.

## Características

- Cálculo automático del diámetro de poleas, longitud de correa, número de correas y factor de seguridad.
- Visualización gráfica de las curvas de rendimiento de la bomba y la resistencia del sistema.
- Interfaz web moderna y fácil de usar (Tailwind CSS).
- Basado en datos y fórmulas de ingeniería reales.

## Uso

1. Instala las dependencias:
   ```
   pip install Flask matplotlib numpy
   ```
2. Ejecuta la aplicación:
   ```
   python app.py
   ```
3. Abre tu navegador en [http://127.0.0.1:5000](http://127.0.0.1:5000) y utiliza la calculadora.

## Estructura

- `app.py`: Código principal de la aplicación Flask y lógica de cálculo.
- Archivos y carpetas adicionales: Documentación técnica, planos, y archivos CAD relacionados con el sistema de bombeo.

## Créditos

- Basado en el libro "Diseño de Elementos de Máquinas" de Mott.
- Datos de bomba: Catálogo Warman WPA43A03.
