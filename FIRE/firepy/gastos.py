import pandas as pd
import altair as alt
import streamlit as st
import numpy as np

## pega o CSV do bunq e transforma o dado

def clean_actual_gastos(df: pd.DataFrame, yaml_dict):

    df["clean_name"] = df["Name"].str.lower()
    df['category'] = "ERR"
    df['Amount'] = df['Amount'].str.replace(".", "")
    df['Amount'] = df['Amount'].str.replace(",", ".")
    df["Amount"] = df["Amount"].astype(float)
    df['Date'] = pd.to_datetime(df["Date"])

    df = df.loc[df["Amount"] <= 0]

    for cat_name, cat_list in yaml_dict.items():
        for store_name in cat_list:
            # print(store_name)
            df['category'] = np.where(
                df["clean_name"].str.contains(store_name.lower()),
                cat_name,
                df['category']
            )


    df['category'] = np.where(
        df["Amount"] > 0,
        "entradas",
        df['category']
    )

    return df

def plot_actual_gastos(df):

    plot_df = df.copy()
    plot_df['anomes'] = plot_df['Date'].dt.year*100 + plot_df['Date'].dt.month
    plot_df['anomes'] = pd.to_datetime(plot_df['anomes'], format="%Y%m")
    plot_df = plot_df.groupby(['anomes', 'category'])[['Amount']].sum().reset_index()


    chart = alt.Chart(plot_df).mark_bar().encode(
        y='sum(Amount)',
        x=alt.X('anomes:T', timeUnit="month"),
        color='category',
        order=alt.Order(
            # Sort the segments of the bars by this field
            'category',
            sort='ascending'
        )
    )

    st.altair_chart(chart, use_container_width=True)
    st.write(df)


def get_custo_moeda(cost_df: pd.DataFrame, config: dict):

    """retorna receita mensal na moeda escolhida"""
    cost_eur = cost_df.loc[cost_df["MOEDA"] == "EUR"]["VALOR"].sum() * (-1)
    cost_brl = cost_df.loc[cost_df["MOEDA"] == "BRL"]["VALOR"].sum() * (-1)
    cost_target = 0
    
    if config["moeda_target"] == "EUR":
        cost_target += cost_brl/config["EUR_to_BRL"]
        cost_target += cost_eur

    elif config["moeda_target"] == "BRL":
        cost_target += cost_eur*config["EUR_to_BRL"]
        cost_target += cost_brl

    return cost_target