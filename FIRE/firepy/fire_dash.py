### Main streamlit app

## a ideia é um dashboard simples, com as principais metricas e graficos para um planejamento financeiro

## Proposito:

## O capitalismo me ensinou a me programar assim. Acho que seria util para as pessoas que, sei la por que motivo
## Se organizariam bem com essa ferramenta

## Filosofia

## Cozinhando para os amigos. Não sou chef de estrela michelin mas sei programar um bom ovo mexido


## No momento discutindo a visão final do produto

### Base timeline/cashflow

### Metricas
    # Dinheiro por conta_tipo por periodo

    # Dinheiro movimentado por conta por periodo
        # Compras onde e quando
        # 

### Base de realizado vs planejado

### Metricas
    # Receitas
        # Salario
        # Investimento
        # Rendas Outras



### Granularidades




import streamlit as st
import pandas as pd
import yaml
from datetime import datetime
from pathlib import Path
import numpy as np
import altair as alt

from receita import get_receita_anualizada, get_receita_moeda
from gastos import clean_actual_gastos, plot_actual_gastos    

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

def calculate_capital_gains(data_df: pd.DataFrame, config: dict):
    """
    Simples e generico, taxa mensal de investimento alteravel
    """

    data_df['CAPITAL_GAINS'] = data_df['PATRIMONIO_INVESTIDO'].shift(1) * config['taxa_investimento']/100
    data_df['CAPITAL_GAINS'] = data_df['CAPITAL_GAINS'].fillna(0)
    return data_df



def calculate_current_balance(data_df: pd.DataFrame, config: dict):
    """
    A partir dos dados de receita e gastos, vai somando o delta e criando
    um balanco para ter noção de patrimonio
    """

    data_df['NET_MENSAL_SALARIO_MENOS_CUSTO'] = data_df['TOTAL_RECEITA_MOEDA'] + data_df['TOTAL_CUSTOS_MOEDA']
    data_df['PATRIMONIO_INVESTIDO'] = data_df['NET_MENSAL_SALARIO_MENOS_CUSTO'].cumsum()

    # add capital inicial
    data_df['PATRIMONIO_INVESTIDO'] = data_df['PATRIMONIO_INVESTIDO'] + 300_000

    data_df = calculate_capital_gains(data_df, config=config)
    data_df['PATRIMONIO_INVESTIDO'] = data_df['PATRIMONIO_INVESTIDO'] + data_df['CAPITAL_GAINS']

    return data_df


def plot_patrimonio(data_df):
    """
    DATA | VALOR | CATEGORIA
    """

    st.write(data_df)

    chart = (
        alt.Chart(data_df)
        .mark_area(opacity=0.3)
        .encode(
            x="DATAS:T",
            y=alt.Y("PATRIMONIO_INVESTIDO:Q"),
            # color="Region:N",
        )
    )
    st.altair_chart(chart, use_container_width=True)


def plot_income_costs(data_df):
    """
    """

    chart = (
        alt.Chart(pd.melt(
            data_df,
            id_vars=['DATAS'],
            value_vars=['NET_MENSAL_SALARIO_MENOS_CUSTO', "CAPITAL_GAINS"]
        ))
        .mark_area(opacity=0.3)
        .encode(
            x="DATAS:T",
            y=alt.Y("value:Q"),
            color="variable:N"
        )
    )
    return st.altair_chart(chart, use_container_width=True)




if __name__ == '__main__':
    st.write("hello world")

    # get_income_data()
    dict_configs = get_configs()['configs']
    dict_cat_gastos = get_configs()['categoria_gastos']
    income_df = get_income_data()
    costs_df = get_costs_data()
    actual_gastos_df = get_actual_gastos(dict_cat_gastos)
    
    dict_configs['taxa_investimento'] = st.slider('Retorno Mensal (%)?', 0.0, 3.0, 0.1)





    # st.write("Receitas", income_df.sort_index())
    st.write("Custos", costs_df.sort_index())



    # create dataframe time series with relevant data
    df_datas = create_timeline_df(dict_configs)
    receita_ano_df = get_receita_anualizada(income_df, df_datas, dict_configs)

    st.write('receita_ano_df:', receita_ano_df)
    st.write('datas:', df_datas)

    df_datas = df_datas.set_index("DATAS").join(
        receita_ano_df.groupby("DATAS")[["TOTAL_RECEITA_MOEDA"]].sum()
    ).reset_index()


    # df_datas["TOTAL_RECEITA_MOEDA"] = 
    df_datas["TOTAL_CUSTOS_MOEDA"] = get_custo_moeda(costs_df, dict_configs)

    # # coloca aposentadoria

    
    df_datas = calculate_current_balance(df_datas, dict_configs)
    
    # configs = st.multiselect(
    #     "Choose CONFIG", list(df_configs.columns), []
    # )


    # st.write("lalala", )


    st.write("Timeline", df_datas.sort_index())

    st.write('Values:', dict_configs['taxa_investimento'])

    plot_patrimonio(df_datas)
    plot_income_costs(df_datas)
    plot_actual_gastos(actual_gastos_df)

