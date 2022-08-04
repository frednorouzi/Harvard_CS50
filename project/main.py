import streamlit as st
from datetime import date
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import yfinance as yf
import numpy as np
import requests
import tweepy
from plotly import graph_objs as go

# get tweeter api key in order to display Tweets about stocks from popular traders on Twitter
consumer_key = 'ZpZYRZSQ3Wasg9qDbincxEjDc'
consumer_secret = 'duL506zrKlCG2VCTUedNtstDPODZaJY8gXLgLK7vGWIvefDyoL'
access_token = '1420132995264958464-1818yePffGJTREMTOdzEmLCseSNFE6'
access_token_secret = 'ywVk1DBX2FlUyc0JEm3eRa8FRF1iOqlEQR4DHlYE3zdkv'

famous_traders = [
'traderstewie',
'the_chart_life',
'canuck2usa',
'sunrisetrader',
'tmltrader',
'SJosephBurns',
'timothysykes',
'StocktonKatie',
'charliebilello',
'NorthmanTrader',
'howardlindzon',
'KeithMcCullough',
'LindaRaschke',
'iancassel'
]

# Creating an OAuthHandler instance (application-user) with an access token
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

st.sidebar.image('fred.png')


st.sidebar.header('Stock Market Web App')

# Create option menue in side bar
option = st.sidebar.selectbox("Select Dashboard", ('General', 'Information', 'Fundamental', 'Twitter', 'Stocktwits', 'News'))

# Reading S&P 500 ticker symbols from text file and adding into variable symbols list
f = open('sandp500_symbols.txt', 'r+')
symbols = []
for row in f:
    symbols.append(row.strip())
f.close()

 # Navigate different options 
if option == 'General':
    # Selected ticker symbol by user
    selected_stock = st.sidebar.selectbox("Select Stock", symbols)
    
    st.subheader(f"{selected_stock} Dashboard")
    # Define starting and ending date of historic stock data
    START = "2014-01-01"
    TODAY = date.today().strftime("%Y-%m-%d")

    # Caching mechanism that allows app to stay performant even when loading data from the web
    @st.cache
    # Loading stock data from Yahoo finance website
    def load_data(ticker):
        data = yf.download(ticker, START, TODAY)
        data.reset_index(inplace=True)
        return data

    data = load_data(selected_stock)

    stock = yf.Ticker(selected_stock)
    if "longName" in stock.info:
        st.write('**_Company_ name:** ', stock.info["longName"])
    if "regularMarketPrice" in stock.info:
        st.write('**_Current_ price:** ', stock.info["regularMarketPrice"])
    if "sector" in stock.info:
        st.write('**_Sector_:** ', stock.info["sector"])
    if "marketCap" in stock.info:
        st.write('**_Market_ Cap:** ', stock.info["marketCap"])
    if "targetLowPrice" in stock.info:
        st.write('**_Target_ Low Price:** ', stock.info["targetLowPrice"])
    if "targetMedianPrice" in stock.info:
        st.write('**_Target_ Median Price:** ', stock.info["targetMedianPrice"])
    if "targetHighPrice" in stock.info:
        st.write('**_Target_ High Price:** ', stock.info["targetHighPrice"])
    if "recommendationKey" in stock.info:
        st.write('**_Recommendation_ Key:** ', stock.info["recommendationKey"])            
    if "longBusinessSummary" in stock.info:
        st.write('**Business summary:** ', stock.info["longBusinessSummary"])

    # Shows historical data of the selected symbol
    st.subheader("Raw Data")    
    st.write(data)
    # Define function to visualize opening and closing price by plotly_chart
    def plot_raw_data():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data["Date"], y=data["Open"], name="stock_open"))
        fig.add_trace(go.Scatter(x=data["Date"], y=data["Close"], name="stock_close"))
        fig.layout.update(title_text=f"Time Series Data", xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)

    plot_raw_data()
    # Define function to visualize volume of the selected ticker by plotly_chart
    def plot_volume_data():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data["Date"], y=data["Volume"], name="stock_volume"))
        fig.layout.update(title_text=f"Time Series Volume Data", xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)

    plot_volume_data()

    # Access selected ticker data
    stock = yf.Ticker(selected_stock)

    # Shows some main shareholders
    st.subheader("Major Holders")
    stock.major_holders

    st.subheader("Institutional Holders")
    stock.institutional_holders

    st.subheader("Recommendations")
    stock.recommendations


if option == 'Twitter':
    st.subheader("Twiter Dashboard")
    # Iterate through the famous_traders
    for username in famous_traders:

        user = api.get_user(username)

        st.header(username)
        st.image(user.profile_image_url)

        tweets = api.user_timeline(username)
        # Manipulating tweet data and cleansing its format to visualize properly  
        for tweet in tweets:
            if '$' in tweet.text:
                words = tweet.text.split(' ')
                for word in words:
                    if word.startswith('$') and word[1:].isalpha():
                        symbol = word[1:]
                        st.write(symbol)
                        st.write(tweet.text)
                        st.image(f"https://finviz.com/chart.ashx?t={symbol}")

if option == 'Information':

    selected_stock = st.sidebar.selectbox("Select Stock", symbols)
    
    stock = yf.Ticker(selected_stock)
    info = str(stock.info)
    info = info.replace(',', '\n')
    st.text(info)
    
if option == 'Fundamental':

    selected_stock = st.sidebar.selectbox("Select Stock", symbols)

    st.image(f"https://finviz.com/chart.ashx?t={selected_stock}")

    stock = yf.Ticker(selected_stock)

    st.subheader(f"Ticker: {selected_stock}")
    st.write('**_Company_ name:** ', stock.info["longName"])

    # Shows fundamental data of the selected ticker
    st.subheader("Dividend, Splits")
    stock.actions

    st.subheader("Earnings")
    stock.earnings

    st.subheader("Quarterly Earnings")
    stock.quarterly_earnings

    st.subheader("Balance Sheet")
    stock.balance_sheet

    st.subheader("Quarterly Balance Sheet")
    stock.quarterly_balance_sheet

    st.subheader("Cash Flow")
    stock.cashflow

    st.subheader("Quarterly Cash Flow")
    stock.quarterly_cashflow
    
    st.subheader("Financials")
    stock.financials

    st.subheader("Quarterly Financials")
    stock.quarterly_financials

if option == 'Stocktwits':

    selected_stock = st.sidebar.selectbox("Select Stock", symbols)

    st.subheader(f"Symbol: {selected_stock}")
    stock = yf.Ticker(selected_stock)
    st.write('**_Company_ name:** ', stock.info["longName"])

    # Retrieving messages using streams/symbols
    r = requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/{selected_stock}.json")
    # Return a JSON object of the data
    data = r.json()
    # Iterate through the data['messages']
    for message in data['messages']:
        st.image(message['user']['avatar_url'])
        st.write(message['user']['username'])
        st.write(message['created_at'])
        st.write(message['body'])

if option == 'News':

    # Parameters 
    n = 20 #the number of article headlines displayed by ticker
    selected_stock = st.sidebar.selectbox("Selected Stock", symbols)

    # Get Data
    finwiz_url = 'https://finviz.com/quote.ashx?t='
    news_tables = {}

    url = finwiz_url + selected_stock
    req = Request(url=url,headers={'user-agent': 'my-app/0.0.1'}) 
    resp = urlopen(req)    
    html = BeautifulSoup(resp, features="lxml")
    news_table = html.find(id='news-table')
    news_tables[selected_stock] = news_table

    try:
        df = news_tables[selected_stock]
        df_tr = df.findAll('tr')
    
        print ('\n')
        print ('Recent News Headlines for {}: '.format(selected_stock))
        
        for i, table_row in enumerate(df_tr):
            a_text = table_row.a.text
            td_text = table_row.td.text
            td_text = td_text.strip()
            print(a_text,'(',td_text,')')
            if i == n-1:
                break
    except KeyError:
        pass

    # Iterate through the news
    parsed_news = []
    for file_name, news_table in news_tables.items():
        for x in news_table.findAll('tr'):
            text = x.a.get_text() 
            date_scrape = x.td.text.split()

            if len(date_scrape) == 1:
                time = date_scrape[0]
                
            else:
                date = date_scrape[0]
                time = date_scrape[1]

            ticker = file_name.split('_')[0]
            
            parsed_news.append([selected_stock, date, time, text])
            
    # Shows the headline of news
    columns = ['Ticker', 'Date', 'Time', 'Headline']
    st.table(pd.DataFrame(parsed_news, columns=columns))