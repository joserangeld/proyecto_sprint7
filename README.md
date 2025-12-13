# proyecto_sprint7
Las tareas de este proyecto incluyen la creación y gestión de entornos virtuales de Python y el desarrollo de una aplicación web. La cual es visible en :

#  Descripción de la aplicación

La aplicación web interactiva construida con **Streamlit** y **Plotly** para la exploración y análisis del conjunto de datos de anuncios de vehículos usados (`vehicles_us.csv`). Permite a los usuarios interactuar con los datos, filtrar por fabricantes y visualizar distribuciones clave como el precio, el millaje (odómetro) y el año del modelo.
La aplicación es visible en https://proyecto-sprint7-xnhs.onrender.com

## Librerias Utilizadas

* **Streamlit:** Para la creación de la interfaz web interactiva.
* **Pandas & NumPy:** Para la carga, limpieza y manipulación de datos.
* **Plotly Express:** Para la generación de gráficos dinámicos e interactivos.

## Características Principales

La aplicación se estructura en varias secciones de análisis:

### 1. Carga y Limpieza de Datos

* Implementación de una función con **`@st.cache_data`** para cargar eficientemente los datos y realizar un proceso de limpieza estandarizado.
* **Tratamiento de Valores Faltantes (NaNs):**
    * Imputación de `is_4wd` con 0.
    * Relleno de `paint_color` con 'unknown'.
    * Imputación de `model_year` y `cylinders` utilizando la mediana agrupada por `model`.
    * Imputación de `odometer` utilizando la mediana agrupada por `model_year` y `condition`.
* Creación de la columna **`manufacturer`** a partir de la primera palabra del campo `model`.

### 2. Visualización y Filtrado de Datos

* **Tabla de Datos Filtrada:** Muestra el DataFrame limpio.
* **Filtro de Frecuencia:** Un *checkbox* permite al usuario excluir fabricantes con menos de 1000 anuncios para enfocarse en las marcas más comunes.

### 3. Distribuciones de Variables Clave

Se utilizan gráficos de barras y de histograma para analizar:
* **Distribución de Tipos de Vehículo:** Conteo total por tipo y segmentación de tipos por fabricante.

### 4. Análisis por Millaje (Odómetro)

* **Diagrama de Dispersión (Precio vs. Odómetro):** Permite ver la relación entre el precio y el kilometraje, con puntos coloreados según la **`condition`** del vehículo.
* **Histograma del Odómetro:** Muestra la distribución general del kilometraje.
* Ambos gráficos pueden ser ocultados/mostrados mediante *checkboxes*.

### 5. Análisis de Antigüedad

* **Histograma de Año del Modelo:** Muestra la distribución de los vehículos por año de fabricación, segmentado por la **`condition`**.

### 6. Análisis Comparativo de Precios

* **Selectores de Fabricantes:** El usuario puede seleccionar dos fabricantes de una lista para realizar una comparación directa.
* **Histograma de Precios Superpuestos:** Muestra la distribución de precios de los dos fabricantes seleccionados en un solo gráfico (utilizando `histnorm='percent'` y `barmode='overlay'`), facilitando la comparación directa de rangos de precios típicos. Los precios extremos se excluyen (percentil 1 y 99) para una mejor visualización.

## 🖥️ Cómo Ejecutar la Aplicación

1.  **Requisitos:** Asegúrate de tener Python instalado.
2.  **Instalar Librerías:**
    ```bash
    pip install streamlit pandas plotly numpy
    ```
3.  **Descargar el Código:** Guarda el código proporcionado en un archivo llamado `app.py` (o similar) y asegúrate de tener el archivo de datos `vehicles_us.csv` en el mismo directorio.
4.  **Ejecutar en la Terminal:**
    ```bash
    streamlit run app.py
    ```
5.  **Abrir en el Navegador:** Streamlit proporcionará una URL local (generalmente `http://localhost:8501`) donde podrás acceder a la aplicación.