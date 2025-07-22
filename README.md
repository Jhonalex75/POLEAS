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
