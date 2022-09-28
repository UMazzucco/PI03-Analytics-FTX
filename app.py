import datetime
import pandas as pd
import requests
from matplotlib import pyplot as plt
import plotly.express as px
import streamlit as st

resolution = 3600
start = datetime.datetime(2022,8,1).timestamp()
end = datetime.datetime.today().timestamp()
api_url = 'https://ftx.com/api'
markets = ['BTC/USD','ETH/USD','USDT/USD','BNB/USD','XRP/USD','SOL/USD','DOGE/USD','DOT/USD','DAI/USD','MATIC/USD']

for coin in markets:
    path = f'/markets/{coin}/candles?resolution={resolution}&start_time={start}&end_time={end}'
    url = api_url + path
    res = requests.get(url).json()
    df = pd.DataFrame(res['result'])
    df['date'] = pd.to_datetime(df['startTime'])
    df = df.set_index('date')
    df = df.drop(columns=['startTime','time'])
    name = coin.replace('/','_')
    df.sort_values('date').to_csv('markets_data/'+name+'.csv')

st.set_page_config(page_title = "Crypto-Analytics",
                   page_icon = ":money_with_wings:",
                   layout='wide')

BTC_USD = pd.read_csv('markets_data/BTC_USD.csv')
ETH_USD = pd.read_csv('markets_data/ETH_USD.csv')
USDT_USD = pd.read_csv('markets_data/USDT_USD.csv')
BNB_USD = pd.read_csv('markets_data/BNB_USD.csv')
XRP_USD = pd.read_csv('markets_data/XRP_USD.csv')
SOL_USD = pd.read_csv('markets_data/SOL_USD.csv')
DOGE_USD = pd.read_csv('markets_data/DOGE_USD.csv')
DOT_USD = pd.read_csv('markets_data/DOT_USD.csv')
DAI_USD = pd.read_csv('markets_data/DAI_USD.csv')
MATIC_USD = pd.read_csv('markets_data/MATIC_USD.csv')

st.title('Análisis de Criptos:')
st.header('Utilizaremos: BTC/USD, ETH/USD, USDT/USD, BNB/USD, XRP/USD, SOL/USD, DOGE/USD, DOT/USD, DAI/USD y MATIC/USD')
st.markdown('Observaremos cada hora desde comienzos de agosto')

st.subheader('BTC/USD:')
st.dataframe(BTC_USD)

st.subheader('ETH/USD:')
st.dataframe(ETH_USD)

st.subheader('USDT/USD:')
st.dataframe(USDT_USD)
