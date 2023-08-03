import streamlit as st
from firepy.front_end.load_graphs import *

if __name__ == "__main__":

    # start_date, end_date = "2018-10-10", "2024-02-08"
    
    # month_list = pd.period_range(start=start_date, end=end_date, freq='M')
    # month_list = [month.strftime("%Y-%m") for month in month_list]
    # print([
    #     d.dt for d in pd.period_range(start=start_date, end=end_date, freq='M')
    # ])

    chart = get_balanco_por_conta(df=None)

    st.altair_chart(chart, use_container_width=True)