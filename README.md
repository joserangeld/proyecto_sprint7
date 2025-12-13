# proyecto_sprint7
Las tareas de este proyecto incluyen la creación y gestión de entornos virtuales de Python y el desarrollo de una aplicación web. 

#  Descripción de la aplicación

La aplicación web permite la exploración y análisis del conjunto de datos de anuncios de vehículos usados (`vehicles_us.csv`),mediante el filtrado por fabricantes y visualización de distribuciones clave como el precio, el millaje (odómetro) y el año del modelo.

La aplicación es visible en https://proyecto-sprint7-xnhs.onrender.com

## Librerias Utilizadas

* **Streamlit:** Para la creación de la interfaz web interactiva.
* **Pandas & NumPy:** Para la carga, limpieza y manipulación de datos.
* **Plotly Express:** Para la generación de gráficos.

## Características Principales

La aplicación se estructura en varias secciones de análisis:

### 1. Carga y Limpieza de Datos

* Implementación de una función con **`@st.cache_data`** para cargar eficientemente los datos y realizar un proceso de limpieza estandarizado.

### 2. Visualización y Filtrado de Datos

* **Tabla de Datos Filtrada:** Muestra el DataFrame limpio.
* **Filtro de Frecuencia:** Un *checkbox* permite al usuario excluir fabricantes con menos de 1000 anuncios para enfocarse en las marcas más comunes.

### 3. Distribuciones por tipo de vehiculo

Se utilizan gráficos de barras para analizar:
* **Distribución de Tipos de Vehículo:** Conteo total por tipo y segmentación de tipos por fabricante.

### 4. Análisis por Millaje (Odómetro)

* **Diagrama de Dispersión (Precio vs. Odómetro):** Permite ver la relación entre el precio y el millaje, con puntos coloreados según la condición del vehículo.
* **Histograma del Odómetro:** Muestra la distribución general del millaje.
* Ambos gráficos pueden ser ocultados/mostrados mediante *checkbox*.

### 5. Análisis de Antigüedad

* **Histograma de Año del Modelo:** Muestra la distribución de los vehículos por año de fabricación, segmentado por la condición del vehiculo y el fabricante.

### 6. Análisis Comparativo de Precios

* **Selectores de Fabricantes:** El usuario puede seleccionar dos fabricantes de una lista para realizar una comparación directa.
* **Histograma de Precios Superpuestos:** Muestra la distribución de precios de los fabricantes seleccionados en un solo gráfico, para la comparación de rangos de precios típicos.
Los precios extremos se excluyen (percentil 1 y 99) para eliminar valores atipicos y tener una mejor visualización.
