# POLEAS – Calculadora de Diseño de Transmisión por Polea y Correa

Aplicación web desarrollada en Python y Flask para el cálculo y visualización del diseño de transmisiones por polea y correa en sistemas de bombeo industrial. Utiliza fórmulas del libro “Diseño de Elementos de Máquinas” de Mott y datos reales de bombas Warman.

## Características

- Cálculo automático de:
  - Diámetro de poleas (motora y conducida)
  - Longitud comercial de correa
  - Número de correas necesarias
  - Factor de seguridad del sistema
- Visualización gráfica de curvas de rendimiento de la bomba y resistencia del sistema
- Interfaz web moderna y responsiva (Tailwind CSS)
- Basado en datos y fórmulas de ingeniería reales

## Estructura del Proyecto

```
POLEAS/
│
├── app/           # Código fuente de la aplicación Flask (app.py)
├── cad/           # Archivos CAD y modelos 3D (.ipt, .iam, .stp, .step, .sat, etc.)
├── calculos/      # Memorias de cálculo y resultados (archivos de texto, hojas de cálculo, etc.)
├── docs/          # Documentación y manuales (PDFs, catálogos)
├── images/        # Imágenes y gráficos (.jpg, .png, etc.)
├── README.md      # Este archivo
└── .gitignore     # (opcional)
```

## Instalación y Ejecución

1. **Clona este repositorio:**
	```bash
	git clone https://github.com/Jhonalex75/POLEAS.git
	cd POLEAS
	```

2. **Instala las dependencias:**
	```bash
	pip install Flask matplotlib numpy
	```

3. **Ejecuta la aplicación:**
	```bash
	python app/app.py
	```

4. **Abre tu navegador en:**
	```
	http://127.0.0.1:5000
	```

## Uso

- Ingresa los datos del motor, bomba y geometría en el formulario web.
- Obtén los resultados de diseño y el gráfico de curvas de la bomba.
- Consulta la documentación técnica y los archivos CAD en las carpetas correspondientes.

## Créditos y Referencias

- Basado en el libro “Diseño de Elementos de Máquinas” de Mott.
- Datos de bomba: Catálogo Warman WPA43A03.
- Interfaz: Tailwind CSS.
