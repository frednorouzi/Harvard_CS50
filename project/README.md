# Stock Market Web Application
#### Video Demo:  [Link](https://www.youtube.com/watch?v=He87rvrmTMU)
#### Description:

I created stock market web app by using streamlit python. The web page include side bar and content page. There are two drop down menu to provide
variety of dashboards and S&P 500 stock ticker symbols. User can easily switch between different dashboards and select specific ticker symbol as well.
The page dynamically loading data from yahoo finance and display proper information in the form of text, chart, image, table, dataframe and dictionary data.
I also registered in twitter developer website to get twitter api key in order to display Tweets about stocks from popular traders on Twitter.

In this project, six dashboards are defined as follows:
* [General](#general)
* [Information](#information)
* [Fundamental](#fundamental)
* [Twitter](#twitter)
* [Stocktwits](#stocktwist)
* [News](#news)

<div id="general"></div>
General:

Display general information about selected ticker symbol such as company name, price, section and brief introduction of the company. It also provide some stock data from
January 2014 until now in data frame format, charts with zoom capability to display daily opening and closing price along with time series volumes data.


<div id="information"></div>
Information:

Provide details financial information about selected ticker as a dictionary format.

The most commonly used keys include the following:

       'language', 'region', 'quoteType', 'triggerable', 'quoteSourceName',
       'currency', 'preMarketChange', 'preMarketChangePercent',
       'preMarketTime', 'preMarketPrice', 'regularMarketChange',
       'regularMarketChangePercent', 'regularMarketTime', 'regularMarketPrice',
       'regularMarketDayHigh', 'regularMarketDayRange', 'regularMarketDayLow',
       'regularMarketVolume', 'regularMarketPreviousClose', 'bid', 'ask',
       'bidSize', 'askSize', 'fullExchangeName', 'financialCurrency',
       'regularMarketOpen', 'averageDailyVolume3Month',
       'averageDailyVolume10Day', 'fiftyTwoWeekLowChange',
       'fiftyTwoWeekLowChangePercent', 'fiftyTwoWeekRange',
       'fiftyTwoWeekHighChange', 'fiftyTwoWeekHighChangePercent',
       'fiftyTwoWeekLow', 'fiftyTwoWeekHigh', 'dividendDate',
       'earningsTimestamp', 'earningsTimestampStart', 'earningsTimestampEnd',
       'trailingAnnualDividendRate', 'trailingPE',
       'trailingAnnualDividendYield', 'marketState', 'epsTrailingTwelveMonths',
       'epsForward', 'sharesOutstanding', 'bookValue', 'fiftyDayAverage',
       'fiftyDayAverageChange', 'fiftyDayAverageChangePercent',
       'twoHundredDayAverage', 'twoHundredDayAverageChange',
       'twoHundredDayAverageChangePercent', 'marketCap', 'forwardPE',
       'priceToBook', 'sourceInterval', 'exchangeDataDelayedBy', 'tradeable',
       'firstTradeDateMilliseconds', 'priceHint', 'exchange', 'shortName',
       'longName', 'messageBoardId', 'exchangeTimezoneName',
       'exchangeTimezoneShortName', 'gmtOffSetMilliseconds', 'market',
       'esgPopulated', 'price'


<div id="fundamental"></div>
Fundamental:

It shows snapshot of latest price chart along with some more important fundamental information such as:
- Dividend, Splits
- Earnings, Quarterly Earnings
- Balance Sheet, Quarterly Balance Sheet
- Cash Flow, Quarterly Cash Flow
- Financials, Quarterly Financials

<div id="twitter"></div>
Twitter:

Displaying Tweets about stocks from popular traders on Twitter along with snapshot of stock price chart which it's coming from finviz website.

<div id="stocktwist"></div>
Stocktwits:

Retrieving messages using streams/symbols and return a JSON object of the data.In this dashboard, you can see tweets from different user that they
talk about that.

<div id="news"></div>
News:

This dashboard provides headline of article news relative to each selected ticker by user.

In addition, The file requirement.txt contains a list of all dependent modules that must be installed before running the program.

Also the list of all ticker symbols of S&P 500 companies are saved in sandp500_symbols.txt file.
In the main file of the Python programming, the text file is read and then all ticker symbols are stored in a list.

### To run application:
##### streamlit run main.py
