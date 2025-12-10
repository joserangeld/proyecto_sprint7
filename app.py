import streamlit as st
import pandas as pd
import plotly.express as px

# Función para cargar y limpiar los datos (replicamos el proceso anterior)
@st.cache_data
def load_and_clean_data(file_path):
    df = pd.read_csv(file_path)

    # 1. Limpieza de 'is_4wd'
    df['is_4wd'] = df['is_4wd'].fillna(0).astype(int)

    # 2. Imputación por mediana agrupada por 'model'
    median_values = df.groupby('model')[['model_year', 'cylinders', 'odometer']].median()
    
    def impute_by_model(row, column, median_df):
        if pd.isnull(row[column]):
            try:
                return median_df.loc[row['model'], column]
            except KeyError:
                return df[column].median()
        return row[column]

    df['model_year'] = df.apply(lambda row: impute_by_model(row, 'model_year', median_values), axis=1)
    df['cylinders'] = df.apply(lambda row: impute_by_model(row, 'cylinders', median_values), axis=1)
    df['odometer'] = df.apply(lambda row: impute_by_model(row, 'odometer', median_values), axis=1)
    
    # 3. Limpieza de 'paint_color'
    df['paint_color'].fillna('unknown', inplace=True)

    # 4. Corrección de tipos de datos y creación de 'manufacturer'
    df['model_year'] = df['model_year'].astype(int)
    df['cylinders'] = df['cylinders'].astype(int)
    df['odometer'] = df['odometer'].astype(int)
    df['date_posted'] = pd.to_datetime(df['date_posted'])
    df['manufacturer'] = df['model'].apply(lambda x: x.split(' ')[0].capitalize())
    
    # Excluir 'unknown' de manufacturer, ya que no son útiles para el análisis
    df = df[df['manufacturer'] != 'Unknown']

    return df

# --- Configuración de la Aplicación Streamlit ---
st.set_page_config(
    page_title="Análisis de Vehículos Usados 🚗", 
    layout="wide"
)

st.title('🚗 Análisis de Vehículos Usados en Venta')
st.markdown('Exploración interactiva del conjunto de datos `vehicles_us.csv`.')

# Cargar los datos limpios
df_clean = load_and_clean_data("vehicles_us.csv")

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