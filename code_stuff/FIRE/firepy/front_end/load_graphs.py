
# Primeiro, precisamos definir quais as analises que queremos ter:


# 1. Dinheiro por conta por periodo
# 2. ?

import altair as alt
import pandas as pd
from faker import Faker
import numpy as np
import streamlit as st

fake = Faker()

def get_balanco_por_conta(
    df: pd.DataFrame,
):
    """
    Retorna o balanco mes a mes de cada conta.
    Idealmente um grafico de linha, com cada conta como uma cor.

    Sei que não vou conseguir todos os dados para todas,
    até por que a Rico acho que no próprio app só tem a partir de 2021.

    Talvez nubank, caixa e itaú tenham. Acho que esses são os principais. Acho que da para pegar de banco do brasil mas faz muito tempo que tenho eles (daria para ver como era minha vida na faculdade, por exemplo)

    df: Table containing the necessary data
    | DATA: datetime
    | VALOR: float
    | NOME_CONTA: str
    """

    # para cada moeda, necessariamente devemos ter todos os valores das, sera que ele aceita nulo = 0? Acho que é bom suficiente
    # preprocessing vai garantir isso dos dados

    if df is None:

        start_date, end_date = "2018-10-10", "2024-02-08"
        month_list = pd.period_range(start=start_date, end=end_date, freq='M')
        # month_list = [month.strftime("%Y-%m") for month in month_list]
        df_datas = pd.DataFrame({
            "DATA": month_list.to_timestamp(),
        })
        df_datas['key'] = 1

        df_contas = pd.DataFrame({
            "NOME_CONTA":["Itau", "Nubank", "bunq", "Santander", "RICO", "Caixa"]
            ,
        })

        df_contas['key'] = 1
        df = df_contas.set_index("key").join(
            df_datas.set_index("key")
        ).reset_index(drop=True)

        df['VALOR'] = np.random.randint(0, high=100, size=df.shape[0], dtype=int)

        st.write(df)

    return alt.Chart(df).mark_area().encode(
        alt.X('DATA:T').axis(format='%Y-%m', domain=False, tickSize=0),
        alt.Y('VALOR:Q').stack('center').axis(None),
        alt.Color('NOME_CONTA:N').scale(scheme='category20b')
    ).interactive()













