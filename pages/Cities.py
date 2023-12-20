import streamlit as st
import plotly.express as px

import pandas as pd
import numpy as np

from PIL import Image
import inflection

st.set_page_config(
    page_title="Visão Cidades",
    page_icon="🏙",
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
df = pd.read_csv('../dataset/zomato.csv')
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
st.header("🏢 Visão Cidades")

# Gráfico de barras: Top 10 cidades com mais restaurantes
grouped_df = (
    df1.loc[df1["country_name"].isin(countries_op), ["restaurant_id", "country_name", "city"]]
    .groupby(["country_name", "city"])
    .count()
    .sort_values(["restaurant_id", "city"], ascending=[False, True])
    .reset_index()
)

fig = px.bar(
    grouped_df.head(10),
    x="city",
    y="restaurant_id",
    text="restaurant_id",
    text_auto=".2f",
    color="country_name",
    title="Top 10 Cidades com mais Restaurantes",
    labels={"city": "Cidade",
            "restaurant_id": "Quantidade de Restaurantes",
            "country_name": "País",
           },
)
st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns( 2 )        

with col1:
    # Gráfico de barras: Top 7 cidades com média de avaliação acima de 4
    grouped_df = (
        df1.loc[
            (df1["aggregate_rating"] >= 4) & (df1["country_name"].isin(countries_op)),
            ["restaurant_id", "country_name", "city"],
        ]
        .groupby(["country_name", "city"])
        .count()
        .sort_values(["restaurant_id", "city"], ascending=[False, True])
        .reset_index()
    )

    fig = px.bar(
        grouped_df.head(7),
        x="city",
        y="restaurant_id",
        text="restaurant_id",
        text_auto=".2f",
        color="country_name",
        title="Top 7 Cidades com Restaurantes com média de avaliação acima de 4",
        labels={
            "city": "Cidade",
            "restaurant_id": "Quantidade de Restaurantes",
            "country_name": "País",
        },
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Gráfico de barras: Top 7 cidades com média de avaliação abaixo de 2.5
    grouped_df = (
        df1.loc[
            (df1["aggregate_rating"] <= 2.5) & (df1["country_name"].isin(countries_op)),
            ["restaurant_id", "country_name", "city"],
        ]
        .groupby(["country_name", "city"])
        .count()
        .sort_values(["restaurant_id", "city"], ascending=[False, True])
        .reset_index()
    )

    fig = px.bar(
        grouped_df.head(7),
        x="city",
        y="restaurant_id",
        text="restaurant_id",
        text_auto=".2f",
        color="country_name",
        title="Top 7 Cidades com Restaurantes com média de avaliação abaixo de 2.5",
        labels={
            "city": "Cidade",
            "restaurant_id": "Quantidade de Restaurantes",
            "country_name": "País",
        },
    )
    st.plotly_chart(fig, use_container_width=True)

# Gráfico de barras: Top 10 cidades com mais tipos de culinárias distintas
grouped_df = (
    df1.loc[df1["country_name"].isin(countries_op), ["cuisines", "country_name", "city"]]
    .groupby(["country_name", "city"])
    .nunique()
    .sort_values(["cuisines", "city"], ascending=[False, True])
    .reset_index()
)

fig = px.bar(
    grouped_df.head(10),
    x="city",
    y="cuisines",
    text="cuisines",
    color="country_name",
    title="Top 10 Cidades mais restaurantes com tipos culinários distintos",
    labels={
        "city": "Cidades",
        "cuisines": "Quantidade de Tipos Culinários Únicos",
        "country_name": "País",
    },
)
st.plotly_chart(fig, use_container_width=True)
