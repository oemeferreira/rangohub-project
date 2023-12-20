import streamlit as st
import plotly.express as px

import pandas as pd
import numpy as np

from PIL import Image
import inflection

st.set_page_config(
    page_title="Visão Países",
    page_icon="🗺",
    layout="wide"
)


# Preenchimento do nome dos países
COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
}
def country_name(country_id):
    return COUNTRIES[country_id]

# Criação do Tipo de Categoria de Comida
def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

# Criação do nome das Cores
COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
}
def color_name(color_code):
    return COLORS[color_code]

# Renomear as colunas do DataFrame
def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df

# Carrregar Dados
df = pd.read_csv('/dataset/zomato.csv')
df1 = df.copy()

# Renomear Colunas
df1 = rename_columns(df1)

#Processar Dados 
df1["price_type"] = df1.loc[:, "price_range"].apply(lambda x: create_price_tye(x))
df1["country_name"] = df1.loc[:, "country_code"].apply(lambda x: country_name(x))
df1["color_name"] = df1.loc[:, "rating_color"].apply(lambda x: color_name(x))

#  Categorizar restaurantes somente por um tipo de culinária
df1["cuisines"] = df1.loc[:, "cuisines"].apply(lambda x: str(x).split(",")[0])

# ===========================
# Side bar
# ===========================
image = Image.open( 'logo.png' )
st.sidebar.image( image, width=160 )

st.sidebar.markdown( "# Encontre. Peça. Viva a Experiência." )
st.sidebar.markdown( """---""" )

# ===========================
# Filtros - Side bar
# ===========================
st.sidebar.markdown( "## Filtros" )
countries_op = st.sidebar.multiselect(
        "Escolha os Paises que Deseja visualizar os Restaurantes",
        df1.loc[:, "country_name"].unique().tolist(),
        default=["Brazil", "England", "Qatar", "South Africa", "Canada", "Australia"],)

# Filtrar dados pelo país selecionado
df1 = df1.loc[df1["country_name"].isin(countries_op), :]

# ===========================
# Página
# ===========================
st.header("🌎 Visão Países")

# Gráfico de barras: Quantidade de restaurantes por país
st.subheader('Quantidade de Restaurantes Registrados por País')
restaurants_per_country = df1['country_name'].value_counts()
st.bar_chart(restaurants_per_country)

# Gráfico de barras: Quantidade de cidades por país
st.subheader('Quantidade de Cidades Registradas por País')
cities_per_country = df1.groupby('country_name')['city'].nunique()
st.bar_chart(cities_per_country)

col1, col2 = st.columns( 2 )

with col1:
    # Gráfico de barras: Média de avaliações por país
    st.subheader('Média de Avaliações Feitas por País')
    avg_ratings_per_country = df1.groupby('country_name')['aggregate_rating'].mean()
    st.bar_chart(avg_ratings_per_country)

with col2:
    # Gráfico de barras: Média de preço de um prato para duas pessoas por país
    st.subheader('Média de Preço de um Prato para Duas Pessoas por País')
    avg_price_per_country = df1.groupby('country_name')['average_cost_for_two'].mean()
    st.bar_chart(avg_price_per_country)
