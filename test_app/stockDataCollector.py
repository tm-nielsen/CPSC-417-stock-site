import yfinance as yf
from django.utils.datetime_safe import strftime
from test_app.API import *
from .models import Stock, Exchange
import datetime
from datetime import datetime


def pullNewStockPrice(ticker):
    stock_info = yf.Ticker(ticker)
    data = stock_info.history()
    last_quote = (data.tail(1)['Close'].iloc[0])
    last_quote = round(last_quote, 2)
    the_stock = StockAPI.get(ticker)
    StockAPI.update_price(the_stock, last_quote)


def addNewStock(ticker):
    try:
        the_stock = yf.Ticker(ticker)
        info = the_stock.info
        current_price = the_stock.history().tail(1)['Close'].iloc[0]
        current_price = round(current_price, 2)
        comp_name = info['shortName']
        div_amount = info['dividendRate']
        ex_dividend_date = None
        exchange_id = info['exchange']
        exchange_timezone = info['exchangeTimezoneName']
        if div_amount is None:
            div_amount = 0
        else:
            ex_dividend_date = datetime.utcfromtimestamp(the_stock.info['lastDividendDate'])
    except ValueError:
        return False
    except KeyError:
        return False
    exchange = ExchangeAPI.get(exchange_id)
    if exchange is None:
        ExchangeAPI.put(exchange_timezone, exchange_id)
    StockAPI.put(comp_name, current_price, ticker, ex_dividend_date, div_amount, exchange_id)
    return True


def addCalls(ticker, expiry_date):
    theStock = yf.Ticker(ticker)
    year = expiry_date.strftime("%Y")
    month = expiry_date.strftime("%m")
    day = expiry_date.strftime("%d")
    the_date = year + '-' + month + '-' + day
    try:
        options = theStock.option_chain(the_date)
    except (ValueError, KeyError, IndexError):
        return False
    calls = options.calls
    prices = calls['strike']
    bids = calls['bid']
    asks = calls['ask']
    premiums = calls['lastPrice']
    j = 0
    for i in calls:
        try:
            CallAPI.put(expiry_date=expiry_date, strike_price=prices[j], bid=bids[j],
                        ask=asks[j], premium=premiums[j], ticker=ticker)
            j = j + 1
        except KeyError:
            j = j + 1
    return True


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
        try:
            current_call = CallAPI.get(expiry_date, prices[j], ticker)
            if current_call is None:
                j = j + 1
                continue
            CallAPI.update_updatable(current_call, bids[j], asks[j], premiums[j])
            j = j + 1
        except KeyError:
            j = j + 1


def addPuts(ticker, expiry_date):
    theStock = yf.Ticker(ticker)
    year = expiry_date.strftime("%Y")
    month = expiry_date.strftime("%m")
    day = expiry_date.strftime("%d")
    the_date = year + '-' + month + '-' + day
    try:
        options = theStock.option_chain(the_date)
    except (ValueError, KeyError, IndexError):
        return False
    puts = options.puts
    prices = puts['strike']
    bids = puts['bid']
    asks = puts['ask']
    premiums = puts['lastPrice']
    j = 0
    for i in puts:
        try:
            PutAPI.put(expiry_date=expiry_date, strike_price=prices[j], bid=bids[j],
                        ask=asks[j], premium=premiums[j], ticker=ticker)
            j = j + 1
        except KeyError:
            j = j + 1
    return True


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
        try:
            current_put = PutAPI.get(expiry_date, prices[j], ticker)
            if current_put is None:
                j = j + 1
                continue
            PutAPI.update_updatable(current_put, bids[j], asks[j], premiums[j])
            j = j + 1
        except KeyError:
            j = j + 1
