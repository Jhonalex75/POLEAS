<<<<<<< HEAD
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
=======
# POLEAS
Calculo de poleas para bomba Warman 4x3

    1 # POLEAS: Recursos de Ingeniería Mecánica
    2
    3 Este repositorio contiene una colección de recursos relacionados con la ingeniería mecánica,
      incluyendo modelos CAD, cálculos de diseño y una aplicación web interactiva.
    4
    5 ## Estructura del Repositorio
    6
    7 El repositorio está organizado de la siguiente manera para facilitar la navegación y el acceso a
      los diferentes tipos de recursos:
    8
    9 *   **`CAD_Files/`**: Contiene todos los modelos y archivos relacionados con el diseño asistido
      por computadora (CAD).
   10     *   **`Assemblies/`**: Ensamblajes de modelos CAD (ej. `.iam`).
   11     *   **`Parts/`**: Componentes individuales de modelos CAD (ej. `.ipt`, `.txt` de
      configuración).
   12     *   **`Libraries/`**: Archivos de librerías o formatos de intercambio CAD (ej. `.SAT`).
   13
   14 *   **`Web_App_Calculations/`**: Contiene aplicaciones web interactivas para cálculos de
      ingeniería.
   15     *   **`calculations.py`**: Módulo con la lógica de cálculo central, utilizada por ambas
      aplicaciones web.
   16     *   **`app.py`**: La aplicación web original basada en Flask, con la interfaz de usuario (
      `index.html`).
   17     *   **`index.html`**: La interfaz de usuario de la aplicación web Flask.
   18     *   **`Web_App_Introduction.ipynb`**: Un Jupyter Notebook que explica el propósito de la
      aplicación web Flask y cómo ejecutarla.
   19     *   **`flet_app.py`**: Una nueva aplicación web interactiva desarrollada con Flet,
      ofreciendo una experiencia de usuario mejorada.
   20     *   **`Flet_App_Introduction.ipynb`**: Un Jupyter Notebook que explica el propósito de la
      aplicación web Flet y cómo ejecutarla.
   21
   22 *   **`docs/`**: Documentación relevante, manuales y catálogos en formato PDF.
   23
   24 *   **`README.md`**: Este archivo, que proporciona una visión general del repositorio.
   25
   26 ## Archivos CAD
   27
   28 Los archivos CAD incluidos en este repositorio son modelos de poleas y componentes relacionados.
      Estos modelos pueden ser utilizados para referencia, estudio o como base para nuevos diseños.
   29
   30 
   32 ## Aplicación Web de Cálculos de Ingeniería
   33
   34 La aplicación web en `Web_App_Calculations/` es una herramienta interactiva que realiza cálculos
      relacionados con el diseño de transmisiones por correa en V y el análisis de curvas de bombas.
      Para aprender cómo ejecutarla y utilizarla, consulta el notebook `Web_App_Introduction.ipynb`
      dentro de esa carpeta.
   35
   36 ## Documentación
   37
   38 La carpeta `docs/` contiene manuales y catálogos que complementan los modelos CAD y los cálculos
      de ingeniería. Por ejemplo:
   39
   40 *   `Manual_poleas_en_V_Intermec.pdf`
   41 *   `qd-bushings-catalog.pdf`
   42
   43 ## Contribuciones
   44
   45 Las contribuciones a este repositorio son bienvenidas. Si deseas añadir nuevos modelos, cálculos
      o mejoras, por favor, abre un "Issue" o envía un "Pull Request".
>>>>>>> 2d1b2cf02961995b1c5a01ea8e2ef04fee7b6650
