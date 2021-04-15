import yfinance as yf
from django.utils.datetime_safe import strftime
from test_app.API import *
from .models import Stock, Exchange
import datetime


def pullNewStockPrice(ticker):
    theStock = yf.Ticker(ticker)
    data = theStock.history()
    last_quote = (data.tail(1)['Close'].iloc[0])
    try:
        theEntry = Stock.objects.get(pk=ticker)
    except(KeyError, Stock.DoesNotExist):
        addNewStock(ticker)
        theEntry = Stock.objects.get(pk=ticker)
    else:
        theEntry.current_value = last_quote
        theEntry.save()


def addNewStock(ticker):
    theStock = yf.Ticker(ticker)
    info = theStock.info
    currentPrice = theStock.history().tail(1)['Close'].iloc[0]
    compName = info['shortName']
    divAmount = info['dividendRate']
    try:
        theExchange = Exchange.objects.get(pk='Placeholder')
    except(KeyError, Exchange.DoesNotExist):
        addNewExchange('Placeholder', 'Placeholder')
        theExchange = Exchange.objects.get(pk='Placeholder')
    s = Stock(name=compName, current_value=currentPrice, ticker=ticker, dividend_date="2000-01-01", dividend_amount=divAmount, exchange_id=theExchange)
    s.save()


def addCalls(ticker, expiry_date):
    theStock = yf.Ticker(ticker)
    year = expiry_date.strftime("%Y")
    month = expiry_date.strftime("%m")
    day = expiry_date.strftime("%d")
    the_date = year + '-' + month + '-' + day
    try:
        options = theStock.option_chain(the_date)
    except ValueError:
        return True
    calls = options.calls
    prices = calls['strike']
    bids = calls['bid']
    asks = calls['ask']
    premiums = calls['lastPrice']
    j = 0
    for i in calls:
        CallAPI.put(expiry_date=expiry_date, strike_price=prices[j], bid=bids[j],
                    ask=asks[j], premium=premiums[j], ticker=ticker)
        j = j + 1


def pull_new_calls_info(ticker, expiry_date):
    theStock = yf.Ticker(ticker)
    year = expiry_date.strftime("%Y")
    month = expiry_date.strftime("%m")
    day = expiry_date.strftime("%d")
    the_date = year + '-' + month + '-' + day
    try:
        options = theStock.option_chain(the_date)
    except ValueError:
        return
    calls = options.calls
    prices = calls['strike']
    bids = calls['bid']
    asks = calls['ask']
    premiums = calls['lastPrice']
    j = 0
    for i in calls:
        current_call = CallAPI.get(expiry_date, prices[j], ticker)
        if current_call is None:
            j = j + 1
            continue
        CallAPI.update_updatable(current_call, bids[j], asks[j], premiums[j])
        j = j + 1


def addPuts(ticker, expiry_date):
    theStock = yf.Ticker(ticker)
    year = expiry_date.strftime("%Y")
    month = expiry_date.strftime("%m")
    day = expiry_date.strftime("%d")
    the_date = year + '-' + month + '-' + day
    try:
        options = theStock.option_chain(the_date)
    except ValueError:
        return True
    puts = options.puts
    prices = puts['strike']
    bids = puts['bid']
    asks = puts['ask']
    premiums = puts['lastPrice']
    j = 0
    for i in puts:
        PutAPI.put(expiry_date=expiry_date, strike_price=prices[j], bid=bids[j],
                    ask=asks[j], premium=premiums[j], ticker=ticker)
        j = j + 1


def pull_new_puts_info(ticker, expiry_date):
    theStock = yf.Ticker(ticker)
    year = expiry_date.strftime("%Y")
    month = expiry_date.strftime("%m")
    day = expiry_date.strftime("%d")
    the_date = year + '-' + month + '-' + day
    try:
        options = theStock.option_chain(the_date)
    except ValueError:
        return
    puts = options.puts
    prices = puts['strike']
    bids = puts['bid']
    asks = puts['ask']
    premiums = puts['lastPrice']
    j = 0
    for i in puts:
        current_put = PutAPI.get(expiry_date, prices[j], ticker)
        if current_put is None:
            j = j + 1
            continue
        PutAPI.update_updatable(current_put, bids[j], asks[j], premiums[j])
        j = j + 1


def addNewExchange(exchangeID, exchangeName):
    ex = Exchange(names='Placeholder', exchange_id='Placeholder')
    ex.save()