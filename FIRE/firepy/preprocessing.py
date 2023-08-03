## main read input and load data

import streamlit as st
from datetime import datetime

import pandas as pd
import numpy as np

import streamlit as st
import pandas as pd
import yaml
from datetime import datetime
from pathlib import Path
import numpy as np
import altair as alt

from firepy.receita import get_receita_anualizada, get_receita_moeda
from firepy.gastos import clean_actual_gastos, plot_actual_gastos


def load_data():
    """
    Objetivo: carregar os principais dados usados para o dash.
    Talvez com o dict só para ser mais fácil
    """
    pass






@st.cache_data
def create_timeline_df(dict_configs):

    initial_year = dict_configs['ano_inicio']
    initial_month = dict_configs['mes_inicio']

    final_year = dict_configs['ano_final']
    final_month = dict_configs['mes_final']

    start_date = datetime.strptime(f"{initial_year}-{initial_month}-01", "%Y-%m-%d")
    final_date = datetime.strptime(f"{final_year}-{final_month}-01", "%Y-%m-%d")

    fut_dates = np.arange(start_date, final_date, dtype="datetime64[M]")

    datas = pd.DataFrame(fut_dates, columns=["DATAS"])
    datas['ANO'] = datas['DATAS'].dt.year
    datas['MES'] = datas['DATAS'].dt.month

    return datas

def get_configs():
    yaml_dict = yaml.safe_load(Path("data/config.yaml").read_text())
    # return df.set_index("settings")
    return yaml_dict

# @st.cache_data
def get_income_data():
    df = pd.read_csv("./data/raw/RECEITA_HOLANDA.csv")
    return df.set_index("NOME_RECEITA")

# @st.cache_data
def get_costs_data():
    df = pd.read_csv("./data/GASTOS_HOLANDA.csv")
    return df.set_index("NOME_CUSTO")

def get_actual_gastos(dict_cat_gastos):
    df = pd.read_csv("./data/raw/vendors/bunq/ExportGastos.csv")
    return clean_actual_gastos(df, dict_cat_gastos)








def base_movimentos_financeiros():
    """
    Controla movimentações de caixa. 
    
    Apenas uma base de dados FATO

    - data_transacao
    - id trancasacao
    - nome_transacao
    - valor
    - conta_referencia
    - tipo_transacao
    - categoria_transacao

    # Puxar dados de alguns lugares:
        # Nubank: (TODO)
        # Santander: (TODO)
        # Itaú: (TODO)
        # Rico: DONE --> export manual
        # bunq: DONE --> export manual
        # Caixa: (TODO)
    """

    pass

def read_bunq_data(config: dict):
    """
    Again, for now, pretty straightforward and POC-like

    Go to bunq website, download account data:

    | Date
    | Interest Date
    | Amount
    | Account (--> muito legal para conta conjunta com minha esposa)
    | Counterparty
    | Name
    | Description
    """

    df = pd.read_csv("./data/gastos/ExportGastos.csv")
    df = clean_actual_gastos_bunq(df, config)

    return df



def clean_actual_gastos_bunq(df: pd.DataFrame, config):

    df["clean_name"] = df["Name"].str.lower()
    df['category'] = "ERR"
    df['Amount'] = df['Amount'].str.replace(".", "")
    df['Amount'] = df['Amount'].str.replace(",", ".")
    df["Amount"] = df["Amount"].astype(float)
    df['Date'] = pd.to_datetime(df["Date"])

    df = df.loc[df["Amount"] <= 0]

    for cat_name, cat_list in config.items():
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


def read_rico_data():
    """
    Versão miojo instantaneo e agile
    Go to RICO website, download account data:

    The guy that made the sheet hates everyone, so he did not upload the actual data, 
    just the kpis in a TERRIBLE format for this. Good pdf, not good sheet

    | 0. Read main secitons
    |   a. Tesouro Direito
    |   b. Fundos Imobiliarios
    |   c. Ações
    |   d. Renda Fixa (CDBs pq nao sei outro nome e vai ficar confuso se for renda fixa)
    |   e. Fundos
    |   f. Proventos (TODO)
    """

    # Como its best to have 1 goHorse 
    # then 1000uselessHorses otimizando segudnos de meses pra frente da minha vida
    # Vou ler a primeira planilha do mes exatamente como ela tá e depois refatoro e generalizo
    #
    # 
    # Vou só anonimizar ela aqui e forcar um to numeric na planilha que é ssó string...1

    # Ajustar path depois de config
    df = pd.read_excel("../../data/vendors/Rico/rico_20230731.xlsx")
    
    # a. tesouro direto:
    tesouro_df = clean_tesouro_direto(df)
    fii_df = clean_fii(df)
    acoes_df = clean_acoes(df)
    cdb_df = clean_CDBS(df) 
    fundo_df = clean_fundos_inv(df)

    return pd.concat([
        tesouro_df,
        fii_df,
        acoes_df,
        cdb_df,
        fundo_df,
    ])

def clean_fii(df: pd.DataFrame) -> pd.DataFrame:
    
    aux_df = df.iloc[22:27, 0:7]
    aux_df.columns = ["NOME_ATIVO", "POSICAO", "PCT_ALOCACAO", "RENTABILIDADE_COM_PROVENTOS", "PRECO_MEDIO", "ULTIMA_COTACAO", "QTD"]
    aux_df['CAT_ATIVO'] = "FII"
    aux_df['TIPO_RENDA'] = "VARIAVEL"

    return aux_df


def clean_acoes(df: pd.DataFrame) -> pd.DataFrame:
    
    aux_df = df.iloc[32:36, 0:7]
    aux_df.columns = ["NOME_ATIVO", "POSICAO", "PCT_ALOCACAO", "RENTABILIDADE_PCT", "PRECO_MEDIO", "ULTIMA_COTACAO", "QTD"]
    aux_df['CAT_ATIVO'] = "ACOES"
    aux_df['TIPO_RENDA'] = "VARIAVEL"

    return aux_df

def clean_renda_fixa(df: pd.DataFrame, coord_dict) -> pd.DataFrame:

    rf_data_columns = ["NOME_ATIVO", "POSICAO", "PCT_ALOCACAO", "TOTAL_APLICADO", "QTD", "DISPONIVEL", "VENCIMENTO"]

    # Sessao Tesouro Direto
    # podia ser loop, mas preguica agora

    fixa_df_pos = df.iloc[coord_dict["pos"][0]:coord_dict["pos"][1], 0:7]
    fixa_df_pos.columns = rf_data_columns
    fixa_df_pos['CAT_ATIVO'] = "TESOURO_DIRETO"
    fixa_df_pos['TIPO_RENDA'] = "POS_FIXADO"

    fixa_df_inflacao = df.iloc[coord_dict["inf"][0]:coord_dict["inf"][1], 0:7]
    fixa_df_inflacao.columns = rf_data_columns
    fixa_df_inflacao['CAT_ATIVO'] = "TESOURO_DIRETO"
    fixa_df_inflacao['TIPO_RENDA'] = "INFLACAO"


    fixa_df_pre = df.iloc[coord_dict["pre"][0]:coord_dict["pre"][1], 0:7]
    fixa_df_pre.columns = rf_data_columns
    fixa_df_pre['CAT_ATIVO'] = "TESOURO_DIRETO"
    fixa_df_pre['TIPO_RENDA'] = "PRE_FIXADO"

    fixa_df = pd.concat([fixa_df_pos, fixa_df_inflacao, fixa_df_pre])

    return fixa_df


def clean_tesouro_direto(df: pd.DataFrame) -> pd.DataFrame:

    coord_dict = {
        "pos": [7,10],
        "inf": [12,14],
        "pre": [16,17]
    }

    return clean_renda_fixa(df, coord_dict)

def clean_CDBS(df: pd.DataFrame) -> pd.DataFrame:
    """A real é que sempre chamei de renda fixa, e é o nome da rico mas vai dar conflito aqui"""
    coord_dict = {
        "pos": [53,60],
        "inf": [41,51],
        "pre": [62,67]
    }

    return clean_renda_fixa(df, coord_dict)

def clean_fundos_inv(df: pd.DataFrame):

    coord_dict = {
        "INTERNACIONAL": [72,75],
        "INFLACAO": [77,78],
        "RENDA_VARIAVEL": [80,81]
    }

    df_list = []

    for k,v in coord_dict.items():
        aux_df = df.iloc[v[0]:v[1], :].copy()
        aux_df.columns = ["NOME_ATIVO", "POSICAO", "PCT_ALOCACAO", "RENTABILIDADE", "VALOR_APLICADO", "VALOR_LIQUIDO", "DATA_COTA"]
        aux_df['CAT_ATIVO'] = "FUNDOS_INVESTIMENTO"
        aux_df['TIPO_FUNDO'] = k
        aux_df['TIPO_RENDA'] = "VARIAVEL"
        df_list.append(aux_df)

    return pd.concat(df_list)

    