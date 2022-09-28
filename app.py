#Importamos lo necesario

import datetime
from re import S
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

#Preparamos la extracción de la data

resolution = 3600
start = datetime.datetime(2022,8,1).timestamp()
end = datetime.datetime.today().timestamp()
api_url = 'https://ftx.com/api'
markets = ['BTC/USD','ETH/USD','USDT/USD','BNB/USD','XRP/USD','SOL/USD','DOGE/USD','DOT/USD','DAI/USD','MATIC/USD']
varianzas = []
conversion_a_usd = []

#Extraemos la data

for coin in markets:
    path = f'/markets/{coin}/candles?resolution={resolution}&start_time={start}&end_time={end}'
    url = api_url + path
    res = requests.get(url).json()
    df = pd.DataFrame(res['result'])
    df['date'] = pd.to_datetime(df['startTime'])
    df = df.drop(columns=['startTime','time'])
    name = coin.replace('/','_')
    df['coin']=str(coin)
    df.sort_values('date',inplace=True)
    df['SMA20'] = round(df['close'].rolling(20).mean())
    df['SMA200'] = round(df['close'].rolling(200).mean())
    df['varianza'] = (df['high'] - df['low'])
    varianzas.append(df.varianza.mean())
    conversion_a_usd.append(float(df.iloc[len(df)-1]['close']))
    df.to_csv('markets_data/'+ name +'.csv')

#Obtenemos y unificamos la data

btc_usd = pd.read_csv('markets_data/BTC_USD.csv')
eth_usd = pd.read_csv('markets_data/ETH_USD.csv')
usdt_usd = pd.read_csv('markets_data/USDT_USD.csv')
bnb_usd = pd.read_csv('markets_data/BNB_USD.csv')
xrp_usd = pd.read_csv('markets_data/XRP_USD.csv')
sol_usd = pd.read_csv('markets_data/SOL_USD.csv')
doge_usd = pd.read_csv('markets_data/DOGE_USD.csv')
dot_usd = pd.read_csv('markets_data/DOT_USD.csv')
dai_usd = pd.read_csv('markets_data/DAI_USD.csv')
matic_usd = pd.read_csv('markets_data/MATIC_USD.csv')
df = pd.concat([btc_usd,eth_usd,usdt_usd,bnb_usd,xrp_usd,sol_usd,doge_usd,dot_usd,dai_usd,matic_usd],ignore_index=True)
df.reset_index(drop=True,inplace=True)
df.drop(columns='Unnamed: 0',inplace=True)

#Creamos la página

st.set_page_config(page_title = "PI03-Crypto-Analytics",
                   page_icon = ":money_with_wings:",
                   layout='wide')

#Establecemos la sidebar

st.sidebar.header("Filtros:")

coin = st.sidebar.selectbox("Seleccione la moneda a observar:" ,df["coin"].unique())

day = str(datetime.datetime(2022,9,1))

data = df.query(
        'coin == @coin & date >= @day')
 

#Título

st.title('Análisis de Criptos:')
st.markdown('Observaremos cada hora desde comienzos de septimbre')

#Figura 1: Candlesticks

fig1 = go.Figure(data=[go.Candlestick(x=data['date'],
                open=data['open'],
                high=data['high'],
                low=data['low'],
                close=data['close'])])

fig1.update_layout(
    title=coin)

# Add range slider
fig1.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=30,
                     label="1m",
                     step="day",
                     stepmode="backward"),
                dict(count=14,
                     label="2w",
                     step="day",
                     stepmode="backward"),
                dict(count=7,
                     label="7d",
                     step="day",
                     stepmode="todate"),
                dict(count=1,
                     label="1d",
                     step="day",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)

#Figura 2: Precio y MA

fig2 = go.Figure(data= go.Scatter(x=data['date'], y=data['close'], mode='lines', name='Price', line_color="#6F6F6F"))

fig2.update_layout(
    title= 'Price and SMAs',
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=30,
                     label="1m",
                     step="day",
                     stepmode="backward"),
                dict(count=14,
                     label="2w",
                     step="day",
                     stepmode="backward"),
                dict(count=7,
                     label="7d",
                     step="day",
                     stepmode="todate"),
                dict(count=1,
                     label="1d",
                     step="day",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)

sma_20 = go.Scatter(x=data['date'], y=data['SMA20'], mode='lines', name='SMA20', line_color="#7DFF03")
sma_200 = go.Scatter(x=data['date'], y=data['SMA200'], mode='lines', name='SMA200', line_color="#FFF703")

fig2.add_trace(sma_20)
fig2.add_trace(sma_200)

#Figura 3: Volumenes de transacción

fig3 = go.Figure(data=go.Bar(x=data['date'], y=data['volume']))

fig3.update_layout(
    title= 'Volumes',
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=30,
                     label="1m",
                     step="day",
                     stepmode="backward"),
                dict(count=14,
                     label="2w",
                     step="day",
                     stepmode="backward"),
                dict(count=7,
                     label="7d",
                     step="day",
                     stepmode="todate"),
                dict(count=1,
                     label="1d",
                     step="day",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)

#Figura 4: Varianza

fig4 = go.Figure(data= go.Bar(x=df['coin'].unique(), y=varianzas, name='Varianza'))
fig4.update_layout(title= 'Varianza')

monedas = df["coin"].unique().tolist()
monedas2 = []
for elem in monedas:
    elem1 = elem.replace('/USD','')
    monedas2.append(elem1)
monedas2.append('USD')
monedas2.append('ARS')
conversion_a_usd.append(float(1))
conversion_a_usd.append(float(1/290))

c1 = st.sidebar.selectbox("Moneda original:" ,monedas2)
c2 = st.sidebar.selectbox("Moneda a convertir:" ,monedas2)
cant = st.sidebar.number_input('Cantidad original:')

def coin_converter(a,b):
    ia = monedas2.index(a)
    ib = monedas2.index(b)
    usd = cant*conversion_a_usd[ia]
    cambio = usd/conversion_a_usd[ib]
    return (cambio)

st.plotly_chart(fig1)
st.plotly_chart(fig2)
st.plotly_chart(fig3)
st.plotly_chart(fig4)
st.sidebar.write('El cambio es:',coin_converter(c1,c2),c2)