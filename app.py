#Importamos lo necesario

import datetime
import pandas as pd
import requests
import plotly.graph_objects as go
import streamlit as st

#Preparamos la extracción de la data

resolution = 3600 #Establecemos como ventana 1 hora
start = datetime.datetime(2022,8,1).timestamp() #Fecha de inicio del análisis (Anterior a la que analizaremos, para los MAs)
end = datetime.datetime.today().timestamp() #Fecha de finalización (Al día)
api_url = 'https://ftx.com/api'

#Armamos las listas que necesitaremos

markets = ['BTC/USD','ETH/USD','USDT/USD','BNB/USD','XRP/USD','SOL/USD','DOGE/USD','DOT/USD','DAI/USD','MATIC/USD'] 
varianza_media = []
varianza_max = []
conversion_a_usd = []
nombres = ['Bitcoin','Ethereum','Tether','BNB','XRP','Solana','Dogecoin','Polkadot','Dai','Polygon']

#Extraemos la data

for coin in markets:
    path = f'/markets/{coin}/candles?resolution={resolution}&start_time={start}&end_time={end}' #Armamos el request
    url = api_url + path #Armamos el url
    res = requests.get(url).json() #Pedimos la data
    df = pd.DataFrame(res['result'])
    df['date'] = pd.to_datetime(df['startTime'])
    df = df.drop(columns=['startTime','time'])
    name = coin.replace('/','_')
    df['coin']=str(coin)
    df.sort_values('date',inplace=True)
    df['SMA20'] = df['close'].rolling(20).mean() #Creamos columna con MA a corto plazo
    df['SMA200'] = df['close'].rolling(200).mean() #Creamos columna con MA a largo plazo
    df['varianza'] = ((((df['high']-df['open']) + (df['open']-df['low']))/2)/df['open']) #Creamos columna spread
    varianza_media.append(df.varianza.mean()*100)#Obtenemos la varianza promedio
    varianza_max.append(df.varianza.max()*100) #Obtenemos la varianza máxima
    conversion_a_usd.append(float(df.iloc[len(df)-1]['close'])) #Agregamos precio actual para el cambio
    df.to_csv('markets_data/'+ name +'.csv') #Guardamos la data

#Obtenemos y unificamos la data

btc_usd = pd.read_csv('markets_data/BTC_USD.csv') #Leemos la data
eth_usd = pd.read_csv('markets_data/ETH_USD.csv')
usdt_usd = pd.read_csv('markets_data/USDT_USD.csv')
bnb_usd = pd.read_csv('markets_data/BNB_USD.csv')
xrp_usd = pd.read_csv('markets_data/XRP_USD.csv')
sol_usd = pd.read_csv('markets_data/SOL_USD.csv')
doge_usd = pd.read_csv('markets_data/DOGE_USD.csv')
dot_usd = pd.read_csv('markets_data/DOT_USD.csv')
dai_usd = pd.read_csv('markets_data/DAI_USD.csv')
shib_usd = pd.read_csv('markets_data/SHIB_USD.csv')

#Creamos un sólo dataframe

df = pd.concat([btc_usd,eth_usd,usdt_usd,bnb_usd,xrp_usd,sol_usd,doge_usd,dot_usd,dai_usd,shib_usd],ignore_index=True)
df.reset_index(drop=True,inplace=True)
df.drop(columns='Unnamed: 0',inplace=True)

#Creamos la página

st.set_page_config(page_title = "PI03-Crypto-Analytics",
                   page_icon = ":money_with_wings:",
                   layout='wide')

coin = st.sidebar.selectbox("Seleccione la moneda a observar:" ,df["coin"].unique()) #Seleccionamos la moneda

start_day = str(datetime.datetime(2022,9,1)) #Día de inicio

data = df.query(
        'coin == @coin & date >= @start_day') #Filtramos el dataframe

st.title('Análisis de Criptomonedas:') #Título
st.markdown('Observaremos cada hora desde comienzos de septimbre')

#Figura 1: Candlesticks

fig1 = go.Figure(data=[go.Candlestick(x=data['date'],
                open=data['open'],
                high=data['high'],
                low=data['low'],
                close=data['close'])])

indice = df["coin"].unique().tolist().index(coin)
nombre = nombres[indice]

fig1.update_layout(
    title=coin+' - '+nombre) #Fijamos Título

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
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)

#Figura 2: Precio y Medias Móviles

fig2 = go.Figure(data= go.Scatter(x=data['date'], y=data['close'], mode='lines', name='Price', line_color="#6F6F6F"))

fig2.update_layout(
    title= 'Precio y Media Móvil',
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
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)

sma_20 = go.Scatter(x=data['date'], y=data['SMA20'], mode='lines', name='MM20', line_color="#7DFF03")
sma_200 = go.Scatter(x=data['date'], y=data['SMA200'], mode='lines', name='MM200', line_color="#FFF703")

fig2.add_trace(sma_20)
fig2.add_trace(sma_200)

#Figura 3: Volumenes de transacción

fig3 = go.Figure(data=go.Bar(x=data['date'], y=data['volume']))

fig3.update_layout(
    title= 'Volumenes',
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
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="date"
    )
)

#Figura 4: Varianza

fig4 = go.Figure(data= go.Bar(x=df['coin'].unique(), y=varianza_media, name='Varianza Porcentual Promedio'))
fig4.update_layout(title= 'Comparación de Varianza Porcentual Promedio')

fig5 = go.Figure(data=go.Bar(x=df['coin'].unique(), y=varianza_max, name='Varianza Porcentual Máxima'))
fig5.update_layout(title= 'Comparación de Varianza Porcentual Máxima')
fig5.update_traces(marker_color='#FF4242')


#Buscaremos el precio de un día

day1 = st.sidebar.date_input('Selecciona una fecha:')
day2 = day1 + datetime.timedelta(days = 1)
dia1 = str(day1)
dia2 = str(day2)

dia = data.query(
        ' date >= @dia1 & date <= @dia2')
st.sidebar.write('El precio de compra fue:',round(dia.high.mean(),2),'USD ')
st.sidebar.write('El precio de venta fue:',round(dia.low.mean(),2),'USD')

#Armaremos la calculadora

monedas = df["coin"].unique().tolist()
monedas2 = []
for elem in monedas:
    elem1 = elem.replace('/USD','')
    monedas2.append(elem1)
monedas2.append('USD')
monedas2.append('ARS')
conversion_a_usd.append(float(1))
conversion_a_usd.append(float(1/150))

c1 = st.sidebar.selectbox("Moneda original:" ,monedas2)
c2 = st.sidebar.selectbox("Moneda a convertir:" ,monedas2)
cant = st.sidebar.number_input('Cantidad:')

def coin_converter(a,b):
    ia = monedas2.index(a)
    ib = monedas2.index(b)
    usd = cant*conversion_a_usd[ia]
    cambio = usd/conversion_a_usd[ib]
    return (cambio)

st.sidebar.write('El cambio es:',coin_converter(c1,c2),c2)

#Imprimiremos todo

st.plotly_chart(fig1)
st.plotly_chart(fig2)
st.plotly_chart(fig3)
st.plotly_chart(fig4)
st.plotly_chart(fig5)
