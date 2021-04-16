from .models import *


class UserAPI:
    @staticmethod
    def get(primary_key):
        try:
            the_user = User.objects.get(pk=primary_key)
        except(KeyError, User.DoesNotExist):
            return None
        else:
            return the_user

    @staticmethod
    def put(username, email, name, password):
        u = User(username=username, email=email, name=name, password=password)
        u.save()

    @staticmethod
    def remove(primary_key):
        the_user = User.objects.get(pk=primary_key)
        the_user.delete()

    @staticmethod
    def getAll():
        u = User.objects.getAll()
        return u


class SurveyAPI:
    @staticmethod
    def get(primary_key):
        try:
            the_survey = Survey.objects.get(pk=primary_key)
        except(KeyError, Survey.DoesNotExist):
            return None
        else:
            return the_survey

    @staticmethod
    def put(date, questions, answer, sentiment, survey_id, u_username, a_username):
        s = Survey(date=date, questions=questions, answer=answer, sentiment=sentiment, survey_id=survey_id, u_username=(UserAPI.get(u_username)), a_username=(AnalystAPI.get(a_username)))
        s.save()

    @staticmethod
    def remove(primary_key):
        the_survey = Survey.objects.get(pk=primary_key)
        the_survey.delete()

    @staticmethod
    def getAll():
        s = Survey.objects.getAll()
        return s


class StockAnalysisAPI:
    @staticmethod
    def get(primary_key):
        try:
            sa = Stock_Analysis.objects.get(pk=primary_key)
        except(KeyError, Stock_Analysis.DoesNotExist):
            return None
        else:
            return sa

    @staticmethod
    def put(title, username, ticker):
        s = Survey(title=(AnalysisAPI.get(title)), username=(AnalystAPI.get(username)), ticker=(StockAPI.get(ticker)))
        s.save()

    @staticmethod
    def remove(primary_key):
        sa = Stock_Analysis.objects.get(pk=primary_key)
        sa.delete()

    @staticmethod
    def getAll():
        sa = Stock_Analysis.objects.getAll()
        return sa


class AnalysisAPI:
    @staticmethod
    def get(primary_key):
        try:
            a = Analysis.objects.get(pk=primary_key)
        except(KeyError, Analysis.DoesNotExist):
            return None
        else:
            return a

    @staticmethod
    def put(description, date, title, username):
        a = Analysis(description=description, date=date, title=title, username=(AnalystAPI.get(username)))
        a.save()

    @staticmethod
    def remove(primary_key):
        a = Analysis.objects.get(pk=primary_key)
        a.delete()

    @staticmethod
    def getAll():
        a = Analysis.objects.getAll()
        return a


class AnalystAPI:
    @staticmethod
    def get(primary_key):
        try:
            a = Analyst.objects.get(pk=primary_key)
        except(KeyError, Analyst.DoesNotExist):
            return None
        else:
            return a

    @staticmethod
    def put(username, email, name, password):
        s = Analyst(username=username, email=email, name=name, password=password)
        s.save()

    @staticmethod
    def remove(primary_key):
        a = Analyst.objects.get(pk=primary_key)
        a.delete()

    @staticmethod
    def getAll():
        a = Analyst.objects.getAll()
        return a


class WatchlistEntryAPI:
    @staticmethod
    def get(ticker, user):
        try:
            we = Watchlist_Entry.objects.get(ticker=ticker, username=user)
        except(KeyError, Watchlist_Entry.DoesNotExist):
            return None
        else:
            return we

    @staticmethod
    def put(username, ticker):
        we = Watchlist_Entry(username=(UserAPI.get(username)), ticker=(StockAPI.get(ticker)))
        we.save()

    @staticmethod
    def remove(primary_key):
        we = Watchlist_Entry.objects.get(pk=primary_key)
        we.delete()

    @staticmethod
    def getAll():
        we = Watchlist_Entry.objects.getAll()
        return we

    @staticmethod
    def get_for_user(user):
        we = Watchlist_Entry.objects.filter(username=user)
        return we


class ViewedHistoryAPI:
    @staticmethod
    def remove(vh):
        vh.delete()

    @staticmethod
    def put(date_viewed, username, ticker):
        vh = Viewed_History(date_viewed=date_viewed, username=(UserAPI.get(username)), ticker=(StockAPI.get(ticker)))
        vh.save()

    @staticmethod
    def get_user_history(username):
        try:
            vh = Viewed_History.objects.filter(username=username).order_by('-date_viewed')
        except(KeyError, Viewed_History.DoesNotExist):
            return None
        else:
            return vh

    @staticmethod
    def getAll():
        vh = Viewed_History.objects.getAll()
        return vh


class ExchangeAPI:
    @staticmethod
    def get(exchange_id):
        try:
            e = Exchange.objects.get(exchange_id=exchange_id)
            return e
        except(KeyError, Exchange.DoesNotExist):
            return None

    @staticmethod
    def put(exchange_timezone, exchange_id):
        e = Exchange(exchange_timezone=exchange_timezone, exchange_id=exchange_id)
        e.save()

    @staticmethod
    def remove(primary_key):
        e = Exchange.objects.get(pk=primary_key)
        e.delete()

    @staticmethod
    def getAll():
        e = Exchange.objects.getAll()
        return e


class StockAPI:
    @staticmethod
    def get(primary_key):
        try:
            the_stock = Stock.objects.get(pk=primary_key)
        except(KeyError, Stock.DoesNotExist):
            return None
        else:
            return the_stock

    @staticmethod
    def put(name, current_value, ticker, ex_dividend_date, dividend_amount, exchange_id):
        s = Stock(name = name, current_value = current_value, ticker = ticker, ex_dividend_date = ex_dividend_date, dividend_amount = dividend_amount, exchange_id = ExchangeAPI.get(exchange_id))
        s.save()

    @staticmethod
    def remove(primary_key):
        the_stock = Stock.objects.get(pk=primary_key)
        the_stock.delete()

    @staticmethod
    def getAll():
        u = Stock.objects.getAll()
        return u

    @staticmethod
    def update_price(stock, price):
        stock.current_value = price
        stock.save()


class PutAPI:
    @staticmethod
    def get(expiry_date, strike_price, ticker):
        try:
            the_put = Put.objects.get(expiry_date=expiry_date, strike_price=strike_price, ticker=ticker)
        except(KeyError, Put.DoesNotExist):
            return None
        else:
            return the_put

    @staticmethod
    def put(expiry_date, strike_price, bid, ask, premium, ticker):
        p = Put(expiry_date=expiry_date, strike_price=strike_price, bid=bid, ask=ask, premium=premium, ticker=StockAPI.get(ticker))
        p.save();

    @staticmethod
    def remove(primary_key):
        the_put = Put.objects.get(pk=primary_key)
        the_put.delete()

    @staticmethod
    def get_expiring_on(ticker, date):
        p = Put.objects.filter(ticker=ticker, expiry_date=date)
        if p.count() == 0:
            return None
        else:
            return p

    @staticmethod
    def getAll():
        u = Put.objects.getAll()
        return u

    @staticmethod
    def update_updatable(put, bid, ask, premium):
        put.bid = bid
        put.ask = ask
        put.premium = premium
        put.save()


class CallAPI:
    @staticmethod
    def get(expiry_date, strike_price, ticker):
        try:
            the_call = Call.objects.get(expiry_date=expiry_date, strike_price=strike_price, ticker=ticker)
        except(KeyError, Call.DoesNotExist):
            return None
        else:
            return the_call

    @staticmethod
    def put(expiry_date, strike_price, bid, ask, premium, ticker):
        c = Call(expiry_date = expiry_date, strike_price = strike_price, bid = bid, ask = ask, premium = premium, ticker= StockAPI.get(ticker))
        c.save()

    @staticmethod
    def remove(primary_key):
        the_call = Call.objects.get(pk = primary_key)
        the_call.delete()

    @staticmethod
    def get_expiring_on(ticker, date):
        c = Call.objects.filter(ticker=ticker, expiry_date=date)
        if c.count() == 0:
            return None
        else:
            return c

    @staticmethod
    def getAll():
        u = Call.objects.getAll()
        return u

    @staticmethod
    def update_updatable(call, bid, ask, premium):
        call.bid = bid
        call.ask = ask
        call.premium = premium
        call.save()


class ValueHistoryAPI:
    @staticmethod
    def get(ticker, date):
        try:
            vh = Value_History.objects.get(ticker=ticker, date=date)
            return vh
        except(KeyError, Value_History.DoesNotExist):
            return None

    @staticmethod
    def put(date, value, ticker):
        vh = Value_History(date=date, value=value, ticker=StockAPI.get(ticker))
        vh.save()



class HistogramAPI:
    @staticmethod
    def get(primary_key):
        try:
            the_Histogram = Histogram.object.get(pk = primary_key)
        except(KeyError, Histogram.DoesNotExist):
            return None
        else:
            return the_Histogram

    @staticmethod
    def put(median, quartiles, id):
        h = Histogram(median = median, quartiles = quartiles, id = id)
        h.save()

    @staticmethod
    def remove(primary_key):
        the_Histogram = Histogram.object.get(pk = primary_key)
        the_Histogram.delete()

    @staticmethod
    def getAll():
        u = Histogram.objects.getAll()
        return u
