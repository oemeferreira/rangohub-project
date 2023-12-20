import streamlit as st
import plotly.express as px

import pandas as pd
import numpy as np

from PIL import Image
import inflection

st.set_page_config(
    page_title="Visão Tipos de Culinárias",
    page_icon="🍝",
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

numero = st.sidebar.slider("Selecione a quantidade de Restaurantes que deseja visualizar", 1, 20, 10)

cuisines = st.sidebar.multiselect( 
    "Escolha os Tipos de Culinária ",
    df1.loc[:, "cuisines"].unique().tolist(),
    default=["Home-made","BBQ","Japanese","Brazilian","Arabian","American","Italian",],)

# Filtrar dados pelo país selecionado
df1 = df1.loc[df1["country_name"].isin(countries_op), :]


# ===========================
# Página
# ===========================
st.header("🍝 Visão Tipos de Culinárias")

cuisines1 = {
    "Italian": "",
    "American": "",
    "Arabian": "",
    "Japanese": "",
    "Brazilian": "",
}

cols = [
    "restaurant_id",
    "restaurant_name",
    "country_name",
    "city",
    "cuisines",
    "average_cost_for_two",
    "currency",
    "aggregate_rating",
    "votes",
]

for key in cuisines1.keys():

    lines = df1["cuisines"] == key

    cuisines1[key] = (
        df1.loc[lines, cols]
        .sort_values(["aggregate_rating", "restaurant_id"], ascending=[False, True])
        .iloc[0, :]
        .to_dict()
    )
# Métricas das principais culinárias
st.markdown("## Melhores Restaurantes dos Principais tipos Culinários")
italian, american, arabian, japanese, brazilian = st.columns(5)

with italian:
    st.metric(
        label=f'Italiana: {cuisines1["Italian"]["restaurant_name"]}',
        value=f'{cuisines1["Italian"]["aggregate_rating"]}/5.0',
        help=f"""
        País: {cuisines1["Italian"]['country_name']}\n
        Cidade: {cuisines1["Italian"]['city']}\n
        Média Prato para dois: {cuisines1["Italian"]['average_cost_for_two']} ({cuisines1["Italian"]['currency']})
        """,
    )

with american:
    st.metric(
        label=f'Americana: {cuisines1["American"]["restaurant_name"]}',
        value=f'{cuisines1["American"]["aggregate_rating"]}/5.0',
        help=f"""
        País: {cuisines1["American"]['country_name']}\n
        Cidade: {cuisines1["American"]['city']}\n
        Média Prato para dois: {cuisines1["American"]['average_cost_for_two']} ({cuisines1["American"]['currency']})
        """,
    )

with arabian:
    st.metric(
        label=f'Arábe: {cuisines1["Arabian"]["restaurant_name"]}',
        value=f'{cuisines1["Arabian"]["aggregate_rating"]}/5.0',
        help=f"""
        País: {cuisines1["Arabian"]['country_name']}\n
        Cidade: {cuisines1["Arabian"]['city']}\n
        Média Prato para dois: {cuisines1["Arabian"]['average_cost_for_two']} ({cuisines1["Arabian"]['currency']})
        """,
    )

with japanese:
    st.metric(
        label=f'Japonesa: {cuisines1["Japanese"]["restaurant_name"]}',
        value=f'{cuisines1["Japanese"]["aggregate_rating"]}/5.0',
        help=f"""
        País: {cuisines1["Japanese"]['country_name']}\n
        Cidade: {cuisines1["Japanese"]['city']}\n
        Média Prato para dois: {cuisines1["Japanese"]['average_cost_for_two']} ({cuisines1["Japanese"]['currency']})
        """,
    )

with brazilian:
    st.metric(
        label=f'Brasileira: {cuisines1["Brazilian"]["restaurant_name"]}',
        value=f'{cuisines1["Brazilian"]["aggregate_rating"]}/5.0',
        help=f"""
        País: {cuisines1["Brazilian"]['country_name']}\n
        Cidade: {cuisines1["Brazilian"]['city']}\n
        Média Prato para dois: {cuisines1["Brazilian"]['average_cost_for_two']} ({cuisines1["Brazilian"]['currency']})
        """,
    )

# Lista com Top Restaurantes
st.markdown(f"## Top {numero} Restaurantes")

cols = [
    "restaurant_id",
    "restaurant_name",
    "country_name",
    "city",
    "cuisines",
    "average_cost_for_two",
    "aggregate_rating",
    "votes",
]

lines = (df1["cuisines"].isin(cuisines)) & (df1["country_name"].isin(countries_op))

df_restaurants = df1.loc[lines, cols].sort_values(
    ["aggregate_rating", "restaurant_id"], ascending=[False, True]
)
st.dataframe(df_restaurants.head(numero))

col1, col2 = st.columns( 2 )

with col1:
    # Gráfico Melhores tipo culinarias
    lines = df1["country_name"].isin(countries_op)

    grouped_df = (
        df1.loc[lines, ["aggregate_rating", "cuisines"]]
        .groupby("cuisines")
        .mean()
        .sort_values("aggregate_rating", ascending=False)
        .reset_index()
        .head(numero)
    )

    fig = px.bar(
        grouped_df.head(numero),
        x="cuisines",
        y="aggregate_rating",
        text="aggregate_rating",
        text_auto=".2f",
        title=f"Top {numero} Melhores Tipos de Culinárias",
        labels={
            "cuisines": "Tipo de Culinária",
            "aggregate_rating": "Média da Avaliação Média",
        },
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Gráfico Piores tipo culinarias
    lines = df1["country_name"].isin(countries_op)

    grouped_df = (
        df1.loc[lines, ["aggregate_rating", "cuisines"]]
        .groupby("cuisines")
        .mean()
        .sort_values("aggregate_rating")
        .reset_index()
        .head(numero)
    )

    fig = px.bar(
        grouped_df.head(numero),
        x="cuisines",
        y="aggregate_rating",
        text="aggregate_rating",
        text_auto=".2f",
        title=f"Top {numero} Piores Tipos de Culinárias",
        labels={
            "cuisines": "Tipo de Culinária",
            "aggregate_rating": "Média da Avaliação Média",
        },
    )
    st.plotly_chart(fig, use_container_width=True)
