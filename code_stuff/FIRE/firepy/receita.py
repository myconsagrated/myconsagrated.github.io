import pandas as pd
import numpy as np

def get_receita_moeda(income_df: pd.DataFrame, config: dict):

    """retorna receita mensal na moeda escolhida"""
    # income_eur = income_df.loc[income_df["MOEDA"] == "EUR"]["VALOR"].sum()
    # income_brl = income_df.loc[income_df["MOEDA"] == "BRL"]["VALOR"].sum()

    income_df["MOEDA_TARGET"] = config["moeda_target"]
    income_df["is_not_in_moeda_target"] = np.where(
        income_df["MOEDA_TARGET"] == income_df["MOEDA"],
        1,
        0
    )

    # income_df["MULTIPLICADOR"]


    if config["moeda_target"] == "EUR":
        income_df["MULTIPLICADOR"] = np.where(
            income_df["MOEDA_TARGET"] == income_df["MOEDA"],
            1,
            1/config["EUR_to_BRL"]
        )
    elif config["moeda_target"] == "BRL":
       income_df["MULTIPLICADOR"] = np.where(
            income_df["MOEDA_TARGET"] == income_df["MOEDA"],
            1,
            1*config["EUR_to_BRL"]
        )
        
    income_df["VALOR_TARGET"] = income_df["VALOR"]*income_df["MULTIPLICADOR"]

    return income_df

def get_if_aposentado(income_df, config):
    income_df["VALOR_TARGET"] = np.where(
        (
            (income_df["DATAS"].min().year + config['anos_trabalho_dani'] >= income_df["DATAS"].dt.year) &
            (income_df['NOME_RECEITA'].str.contains("DANI"))
        ) | (
            (income_df["DATAS"].min().year + config['anos_trabalho_gabi'] >= income_df["DATAS"].dt.year) &
            (income_df['NOME_RECEITA'].str.contains("GABI"))
        ),
        income_df["VALOR_TARGET"],
        0
    )

    return income_df


def get_receita_anualizada(income_df: pd.DataFrame, time_df: pd.DataFrame, config: dict):
    """
    """

    df = time_df.copy()
    df['key'] = 1
    income_df = income_df.reset_index()
    income_df['key'] = 1

    df = df.set_index("key").join(income_df.set_index("key")).reset_index()

    df = get_receita_moeda(df, config)
    df = get_if_aposentado(df, config)

    df['TOTAL_RECEITA_MOEDA'] = df["VALOR_TARGET"]

    return df