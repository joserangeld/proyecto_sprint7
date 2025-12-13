import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# -----------------1.Función para cargar y limpiar los datos (se copia el proceso de EDA.ipynb)--------------
@st.cache_data
def load_and_clean_data(file_path):
    car_data = pd.read_csv(file_path)

   # 1. Tratar la columna `is_4wd` Los nulos representan la ausencia de 4WD, por lo que se rellenan con 0.0
    car_data['is_4wd'] = car_data['is_4wd'].fillna(0.0).astype(int)

    # 2. Tratar la columna `paint_color` Rellenar nulos con una categoría 'unknown'
    car_data['paint_color'] = car_data['paint_color'].fillna('unknown')

    # 3. Tratar `model_year` y `cylinders` Imputar nulos con la mediana del grupo 'model'
    car_data['model_year'] = car_data.groupby('model')['model_year'].transform(lambda x: x.fillna(x.median()))
    car_data['cylinders'] = car_data.groupby('model')['cylinders'].transform(lambda x: x.fillna(x.median()))

    # 4. Tratar `odometer`. Imputar nulos con la mediana del grupo de 'model_year' y 'condition'
    car_data['odometer'] = car_data.groupby(['model_year', 'condition'])['odometer'].transform(lambda x: x.fillna(x.median()))
   
   # 5. Convertir columnas a enteros (después de imputar los nulos en `model_year` y `cylinders`)
    int_cols = ['price', 'model_year', 'cylinders', 'odometer']
    for col in int_cols:
        car_data[col] = car_data[col].round(0).astype('Int64') # Int64 maneja valores NaN como nulos

    # 6. Crear la columna 'manufacturer' a partir de 'model' (primer palabra) 
    car_data['manufacturer'] = car_data['model'].apply(lambda x: x.split(' ')[0].capitalize())
   
    return car_data

# --------------------2. Configuración de la Aplicación Streamlit ------------

st.set_page_config(
    page_title="Análisis de Vehículos Usados ", 
    layout="wide"
)
st.title(' Análisis de Vehículos Usados en Venta')
st.markdown('Exploración interactiva del conjunto de datos `vehicles_us.csv`.')

# Cargar los datos limpios
car_clean = load_and_clean_data('vehicles_us.csv')


#--------2.1 Visualización de Datos Limpios ------------
manufacturer_counts = car_clean['manufacturer'].value_counts()
MIN_ADS = 1000
low_freq_manufacturers = manufacturer_counts[manufacturer_counts < MIN_ADS].index.tolist()
high_freq_manufacturers = manufacturer_counts[manufacturer_counts >= MIN_ADS].index.tolist()

show_low_freq = st.checkbox(
    f'Incluir Fabricantes con menos de {MIN_ADS} anuncios (Marcas Menos Comunes)',
    value=False, # Por defecto, NO se muestran (True = se muestran)
    help='Si se desmarca, se muestran todos los fabricantes.'
)
if  show_low_freq:
      car_filtered = car_clean
else:
      car_filtered = car_clean[car_clean['manufacturer'].isin(high_freq_manufacturers)]

st.dataframe(car_filtered)
st.markdown(f"Mostrando **{len(car_filtered)}** registros de **{len(car_clean)}** en total.")    


#-------- 2.2 Distribuciones de por tipo de vehículo -----
st.subheader('Conteo por Tipo de Vehículo')
col1, col2 = st.columns(2)

with col1:
    # Gráfico de barras para el fabricante
    type_grouped = car_clean.groupby(['manufacturer', 'type']).size().reset_index(name='count')
    fig = px.bar(
        type_grouped,
        x='manufacturer',
        y='count',
        color='type',
        title='Distribución de Tipos de Vehículo por Fabricante',
        labels={'manufacturer': 'Fabricante','count': 'Cantidad de Vehículos','type': 'Tipo de Vehículo'}
    )
    
    st.plotly_chart(fig, use_container_width=True)  

with col2:  
    # Gráfico de barras para el tipo de vehículo
    type_counts = car_clean['type'].value_counts().reset_index()
    type_counts.columns = ['Type', 'Count']
    
    fig_type_count = px.bar(
        type_counts,
        x='Type',
        y='Count',
        orientation='v',
        color='Type',
    title='Número de Anuncios por Tipo de Vehículo',
    labels={'Count': 'Número de Vehículos', 'Type': 'Tipo de Vehículo'}
    )
    st.plotly_chart(fig_type_count, use_container_width=True)

# -------2.3 Checkbox para mostrar/ocultar el diagrama de dispersión -------
st.subheader('Análisis por Millaje (Odómetro)')
col1, col2 = st.columns(2)
with col1:
    show_scatter = st.checkbox(
        'Mostrar Diagrama de Dispersión: Precio vs. Odómetro', 
    value=True
)
    if show_scatter:   
        # Diagrama de dispersión: Precio vs Odómetro, coloreado por Condición
        fig_scatter = px.scatter(
            car_clean,
            x='odometer',
            y='price',
            color='condition',
            hover_data=['model', 'manufacturer'],
        title='Precio vs. Millaje por Condición',
        labels={'odometer': 'Millaje (Millas)', 'price': 'Precio ($)'}
    )
        st.plotly_chart(fig_scatter, use_container_width=True)

with col2:
    show_hist = st.checkbox(
        'Mostrar Histograma: Odómetro', 
    value=True
)
    if show_hist:   
        # Histograma de Odómetro
        fig = px.histogram(
            car_clean, x='odometer',
            title='Distribución de Millaje de Vehículos',
            labels={'odometer': 'Millaje (Millas)', 'count': 'Frecuencia'}
            ) # crear un histograma
        st.plotly_chart(fig, use_container_width=True)


# -------2.4 Distribución de Antigüedad del Vehículo ------

st.subheader('Análisis de Antigüedad')
col1, col2 = st.columns(2)

with col1:
    # Gráfico de barras para model_year
       
    fig_year_bar = px.histogram(
        car_clean,
        x='model_year',
        nbins=100,
        color = 'condition',
        title='Condición de Vehículos por Año del Modelo',
        labels={'model_year': 'Año del Modelo', 'condition': 'Condición'}
    )
    st.plotly_chart(fig_year_bar, use_container_width=True)

with col2:  
    # Gráfico de histograma para model_year
    fig_year_hist = px.histogram(
        car_clean,
        x='model_year',
        nbins=50,
        color='manufacturer',
        title='Distribución de Vehículos por Año del Modelo',
        labels={'model_year': 'Año del Modelo', 'count': 'Frecuencia'},
    
    )
    st.plotly_chart(fig_year_hist, use_container_width=True)


#------ 2.5 Análisis comparativo de Precios ----------
st.subheader('Análisis comparativo de Precios')

# Crear la lista de fabricantes con nombres estandarizados
manufacturer_mapping = {
        'Chevrolet': 'Chevrolet', 'Gmc': 'GMC', 'Bmw': 'BMW', 'Ford': 'Ford'
    }
car_clean['manufacturer'] = car_clean['manufacturer'].replace(manufacturer_mapping)

# Definir las Opciones de Selección
all_manufacturers = sorted(car_clean['manufacturer'].unique())

#  Selectbox para la Selección del Usuario
col1, col2 = st.columns(2)

with col1:
    manufacturer_1 = st.selectbox(
        'Selecciona el Fabricante 1 (Color Azul):',
        options=all_manufacturers,
        index=all_manufacturers.index('Ford') if 'Ford' in all_manufacturers else 0,
        key='mfg1'
    )

with col2:
    # Usamos un valor por defecto diferente para el segundo, si es posible
    default_index_2 = all_manufacturers.index('Chevrolet') if 'Chevrolet' in all_manufacturers else (1 if len(all_manufacturers) > 1 else 0)
    manufacturer_2 = st.selectbox(
        'Selecciona el Fabricante 2 (Color Naranja):',
        options=all_manufacturers,
        index=default_index_2,
        key='mfg2'
    )

#  Lógica de Filtrado y Visualización. combinar las dos selecciones en una lista
selected_manufacturers = [manufacturer_1, manufacturer_2]

if manufacturer_1 == manufacturer_2:
    st.warning(" Por favor, selecciona **dos fabricantes diferentes** para realizar una comparación válida.")
else:
    # Filtrar el DataFrame para incluir solo los fabricantes seleccionados
    car_compare = car_clean[car_clean['manufacturer'].isin(selected_manufacturers)]

    # Determinar el rango de precios (excluyendo precios extremos, posibles atipicos)
    price_max = car_compare['price'].quantile(0.99)
    price_min = car_compare['price'].quantile(0.01)

    #crear un mapa de colores personalizado ( en la prueba los dos se mostraban azules)
    color_map = {
        manufacturer_1: '#1f77b4',  # Azul (Color 1)
        manufacturer_2: "#f9ba1b"   # Rojo (Color 2)
    }
    
    # Crear el Histograma 
    fig = px.histogram(
        car_compare,
        x='price',
        color='manufacturer',
        nbins=100,
        histnorm='percent',
        title=f'Distribución de Precios: {manufacturer_1} vs {manufacturer_2}',
        labels={'price': 'Precio (USD)', 'count': 'Frecuencia', 'manufacturer': 'Fabricante'},
        opacity=0.65,
        barmode='overlay',
        range_x=[price_min, price_max],
        color_discrete_map=color_map
    )

    fig.update_layout(yaxis_title="Porcentaje de Anuncios", legend_title_text="Fabricante")

    # 6. Mostrar el Gráfico en Streamlit
    st.plotly_chart(fig, use_container_width=True)



# -------------------Final de la Aplicación Streamlit ------------------

st.markdown("---")
st.markdown("Realizado por: José Alfredo Rangel Deantes")