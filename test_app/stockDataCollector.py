import yfinance as yf
from .models import Stock, Exchange

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


def addCalls(ticker):
    theStock = yf.Ticker(ticker)
    print("please")
    print(theStock.options)


def addNewExchange(exchangeID, exchangeName):
    ex = Exchange(names='Placeholder', exchange_id='Placeholder')
    ex.save()