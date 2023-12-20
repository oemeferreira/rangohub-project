import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
import folium

from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
from PIL import Image
import inflection

st.set_page_config(
    page_title="Home",
    page_icon="📊",
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
df = pd.read_csv('dataset/zomato.csv')
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


# ===========================
# Página
# ===========================

st.markdown(
    """
    # 📊 RangoHub
    ##  O Melhor lugar para encontrar seu mais novo restaurante favorito!
    ### Temos as seguintes marcas dentro da nossa plataforma:
""" )
rm = df1.loc[:, "votes"].sum()

restaurants, countries, cities, ratings, cuisines = st.columns(5)

restaurants.metric("Restaurantes Cadastrados", df1.shape[0])
countries.metric("Países Cadastrados",df1.loc[:, "country_code"].nunique())
cities.metric("Cidades Cadastrados",df1.loc[:, "city"].nunique())
ratings.metric("Avaliações Feitas na Plataforma",f"{rm:,}".replace(",", "."))
cuisines.metric("Tipos de Culinárias Oferecidas", df1.loc[:, "cuisines"].nunique())


df_aux = df1.loc[df1["country_name"].isin(countries_op), :]

f = folium.Figure(width=1920, height=1080)

m = folium.Map(max_bounds=True).add_to(f)

marker_cluster = MarkerCluster().add_to(m)

for _, line in df_aux.iterrows():

    name = line["restaurant_name"]
    price_for_two = line["average_cost_for_two"]
    cuisine = line["cuisines"]
    currency = line["currency"]
    rating = line["aggregate_rating"]
    color = f'{line["color_name"]}'

    html = "<p><strong>{}</strong></p>"
    html += "<p>Price: {},00 ({}) para dois"
    html += "<br />Type: {}"
    html += "<br />Aggragate Rating: {}/5.0"
    html = html.format(name, price_for_two, currency, cuisine, rating)

    popup = folium.Popup(
        folium.Html(html, script=True),
        max_width=500,
    )

    folium.Marker(
        [line["latitude"], line["longitude"]],
        popup=popup,
        icon=folium.Icon(color=color, icon="home", prefix="fa"),
    ).add_to(marker_cluster)

folium_static(m, width=1024, height=768)

