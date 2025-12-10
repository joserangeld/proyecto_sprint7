import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Función para cargar y limpiar los datos (se copia el proceso de EDA.ipynb)
@st.cache_data
def load_and_clean_data(file_path):
    car_data = pd.read_csv(file_path)

   # 1. Manejar 'is_4wd': Rellenar NaN con 0 y convertir a int
    car_data['is_4wd'] = car_data['is_4wd'].fillna(0).astype(int)

    # 2. Imputar 'model_year', 'cylinders' y 'odometer' usando la mediana por 'model'

    # Calcular la mediana de estas columnas agrupadas por 'model'
    median_values = car_data.groupby('model')[['model_year', 'cylinders', 'odometer']].median()

    # Función para rellenar NaN con el valor mediano del modelo
    def impute_by_model(row, column, median_df):
        if pd.isnull(row[column]):
        # Intenta obtener la mediana para el modelo actual, si existe
            try:
             return median_df.loc[row['model'], column]
            except KeyError:
            # Si el modelo no está en el índice de medianas (caso raro), devuelve NaN temporalmente
             return np.nan 
        return row[column]

    car_data['model_year'] = car_data.apply(lambda row: impute_by_model(row, 'model_year', median_values), axis=1)
    car_data['cylinders'] = car_data.apply(lambda row: impute_by_model(row, 'cylinders', median_values), axis=1)
    car_data['odometer'] = car_data.apply(lambda row: impute_by_model(row, 'odometer', median_values), axis=1)

    # Imputación de 'model_year', 'cylinders' y 'odometer' con la mediana global restante
    # (Para los casos donde el modelo en sí mismo tiene NaN, ya que no se encontró mediana)
    car_data['model_year'].fillna(car_data['model_year'].median(), inplace=True)
    car_data['cylinders'].fillna(car_data['cylinders'].median(), inplace=True)
    car_data['odometer'].fillna(car_data['odometer'].median(), inplace=True)

    # 3. Manejar 'paint_color': Rellenar NaN con 'unknown'
    car_data['paint_color'].fillna('unknown', inplace=True)

    # 4. Corregir tipos de datos
    car_data['model_year'] = car_data['model_year'].astype(int)
    car_data['cylinders'] = car_data['cylinders'].astype(int)
    car_data['odometer'] = car_data['odometer'].astype(int)
    car_data['date_posted'] = pd.to_datetime(car_data['date_posted'])
    # Crear la columna 'manufacturer' a partir de 'model' (primer palabra) para filtros útiles
    car_data['manufacturer'] = car_data['model'].apply(lambda x: x.split(' ')[0].capitalize())

    return car_data

# --- Configuración de la Aplicación Streamlit ---
st.set_page_config(
    page_title="Análisis de Vehículos Usados ", 
    layout="wide"
)

st.title(' Análisis de Vehículos Usados en Venta')
st.markdown('Exploración interactiva del conjunto de datos `vehicles_us.csv`.')

# Cargar los datos limpios
df_clean = load_and_clean_data('vehicles_us.csv')

# --- Barra Lateral (Filtros) ---
st.sidebar.header('Filtros y Controles')

# Filtro 1: Fabricante (Marca)
selected_manufacturers = st.sidebar.multiselect(
    'Selecciona el Fabricante:',
    options=df_clean['manufacturer'].unique(),
    default=df_clean['manufacturer'].unique()[:5] # Seleccionar los 5 primeros por defecto
)

df_filtered = df_clean[df_clean['manufacturer'].isin(selected_manufacturers)]

# Filtro 2: Precio (Rango deslizante)
min_price = int(df_filtered['price'].min())
max_price = int(df_filtered['price'].max())
price_range = st.sidebar.slider(
    'Rango de Precio ($):',
    min_value=min_price,
    max_value=max_price,
    value=(min_price, max_price),
    step=1000
)

df_filtered = df_filtered[
    (df_filtered['price'] >= price_range[0]) & 
    (df_filtered['price'] <= price_range[1])
]

st.sidebar.metric(
    label="Vehículos Seleccionados",
    value=f"{len(df_filtered):,}"
)

# --- Contenido Principal ---

st.header('Resumen de los Datos Filtrados')
st.dataframe(df_filtered.head())
st.markdown(f"Mostrando **{len(df_filtered)}** registros de **{len(df_clean)}** en total.")

# --- Distribuciones de Variables Clave (Columnas) ---

col1, col2 = st.columns(2)

with col1:
    st.subheader('Distribución de Precio por Condición')
    
    # Gráfico de violín o caja para ver la distribución del precio por condición
    fig_price_condition = px.box(
        df_filtered, 
        x='condition', 
        y='price',
        color='condition',
        title='Distribución de Precio',
        labels={'price': 'Precio ($)', 'condition': 'Condición del Vehículo'},
        category_orders={"condition": ["new", "like new", "excellent", "good", "fair", "salvage"]}
    )
    st.plotly_chart(fig_price_condition, use_container_width=True)

with col2:
    st.subheader('Conteo por Tipo de Vehículo')
    
    # Gráfico de barras para el tipo de vehículo
    type_counts = df_filtered['type'].value_counts().reset_index()
    type_counts.columns = ['Type', 'Count']
    
    fig_type_count = px.bar(
        type_counts,
        x='Count',
        y='Type',
        orientation='h',
        color='Type',
        title='Número de Anuncios por Tipo de Vehículo',
        labels={'Count': 'Número de Vehículos', 'Type': 'Tipo de Vehículo'}
    )
    st.plotly_chart(fig_type_count, use_container_width=True)

# --- Relación entre Variables ---

st.header('Relación entre Variables')

# Widget de checkbox para mostrar/ocultar el scatter plot
show_scatter = st.checkbox(
    'Mostrar Diagrama de Dispersión: Precio vs. Odómetro', 
    value=True
)

if show_scatter:
    st.subheader('Precio vs. Odómetro (Kilometraje)')
    
    # Diagrama de dispersión: Precio vs Odómetro, coloreado por Condición
    fig_scatter = px.scatter(
        df_filtered,
        x='odometer',
        y='price',
        color='condition',
        hover_data=['model', 'manufacturer'],
        title='Precio vs. Kilometraje por Condición',
        labels={'odometer': 'Kilometraje (Millas)', 'price': 'Precio ($)'}
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# --- Distribución de Antigüedad del Vehículo ---

st.header('Análisis de Antigüedad')
# Gráfico de histograma para model_year
fig_year_hist = px.histogram(
    df_filtered,
    x='model_year',
    nbins=50,
    color='fuel',
    title='Distribución de Vehículos por Año del Modelo',
    labels={'model_year': 'Año del Modelo', 'count': 'Frecuencia'},
    height=400
)
st.plotly_chart(fig_year_hist, use_container_width=True)