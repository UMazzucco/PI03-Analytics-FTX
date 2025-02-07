# PI03 - Analytics

<img src='https://user-images.githubusercontent.com/103452945/235523906-1f61fefb-7624-4445-ae5f-0e884609645c.png' width='50' height='50'> <img src='https://user-images.githubusercontent.com/103452945/235524753-f95f11fa-7e22-48c5-af5e-59958c487e81.svg' width='125' height='50'> <img src='https://user-images.githubusercontent.com/103452945/235524029-b3882169-c909-410a-be79-958aefa4c653.png' width='50' height='50'> <img src='https://user-images.githubusercontent.com/103452945/235523917-9ee94b84-f5b6-49ed-b801-df814d319814.png' width='50' height='50'> <img src='https://user-images.githubusercontent.com/103452945/235469235-3c78abd3-dfd3-4755-bcc2-192b8fdfe4b9.png' width='125' height='50'> 

## About

Este es mi 3er Proyecto Individual para el curso de Data Science de Henry.

En un dashboard en Streamlit mostraremos la fluctuación de precios, volúmenes de transacción, varianza porcentual promedio, y máxima y medias móviles a 20 y a 200 períodos.

Utilicé el período desde comienzos de septiembre, y nuestra ventana será de una hora.

Seleccionamos las criptomonedas que cuenten con mayor capitalización de mercado al momento según <https://coinmarketcap.com/es/> , con mercado respecto al dólar en FTX. Todos los mercados operan.

Agregamos también un selector para consultar los precios de la criptomoneda deseada un día en particular y una calculadora que nos permitirá convertir entre criptomonedas, dólares y pesos argentinos.

Se expuso además una breve explicación sobre la fluctuación del precio de Ethereum desde el análisis fundamental.

### Lista de mercados

Bitcoin (BTC), Ethereum (ETH), Tether (USDT), BNB, XRP, Solana (SOL), Dogecoin (DOGE), Polkadot (DOT), Dai (DAI) y Polygon (MATIC)

## Dashboard

La aplicación funcionaba en <https://umazzucco-pi03-analytics-ftx-app-9klilj.streamlitapp.com/>  
Sin embargo, debido a la caída de la API de FTX por cuestiones legales, está fuera de funcionamiento. Más información sobre el caso en <https://www.investopedia.com/what-went-wrong-with-ftx-6828447>

## Análisis

El análisis se centró en buscar los momentos con subidas y caídas más abruptas, en busca de hitos que nos permitieran, desde el análisis fundamental de mercado, predecir la tendencia a nivel general. Investigando dichas caídas encontramos coincidencias con diversos hitos, como el proceso de migración del sistema de Ethereum (y el consecuente impedimento al minado de dicha criptomoneda) la suba de las tasas bancarias en Estados Unidos y la revelación de la inflación para dicho mes en el mismo país. Todos estos momentos generaron desconfianza y forzaron la venta de la divisa, que posteriormente se estabilizaba con un rebote.

## Links de interés (Análisis Ethereum)

Merge Ethereum: <https://blog.ethereum.org/2022/08/24/mainnet-merge-announcement>

FOMC Fund Rate Increase: <https://www.forbes.com/advisor/investing/fomc-meeting-federal-reserve/#:~:text=The%20Federal%20Open%20Market%20Committee,rate%20increase%20this%20year%20alone.>

13 Sept Volatility: <https://u.today/september-13-is-crucial-date-for-cryptocurrency-market-and-not-only-because-of-ethereum-merge#h20>

US CPI: <https://ycharts.com/indicators/us_inflation_rate#:~:text=US%20Inflation%20Rate%20is%20at,long%20term%20average%20of%203.26%25.>
