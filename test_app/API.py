from .models import *

class UserAPI:
    def get(self, primary_key):
        try:
            the_user = User.objects.get(pk=primary_key)
        except(KeyError, User.DoesNotExist):
            return None
        else:
            return the_user


    def put(self, username, email, name, password):
        u = User(username=username, email=email, name=name, password=password)
        u.save()

    def remove(self, primary_key):
        the_user = User.objects.get(pk=primary_key)
        the_user.delete()

    def getAll(self):
        u = User.objects.getAll()
        return u



class SurveyAPI:
    def get(self, primary_key):
        try:
            the_survey = Survey.objects.get(pk=primary_key)
        except(KeyError, Survey.DoesNotExist):
            return None
        else:
            return the_survey


    def put(self, date, questions, answer, sentiment, survey_id, u_username, a_username):
        s = Survey(date=date, questions=questions, answer=answer, sentiment=sentiment, survey_id=survey_id, u_username=(UserAPI.get(u_username)), a_username=(AnalystAPI.get(a_username)))
        s.save()

    def remove(self, primary_key):
        the_survey = Survey.objects.get(pk=primary_key)
        the_survey.delete()

        def getAll(self):
            s = Survey.objects.getAll()
            return s


class Stock_AnalysisAPI:
    def get(self, primary_key):
        try:
            sa = Stock_Analysis.objects.get(pk=primary_key)
        except(KeyError, Stock_Analysis.DoesNotExist):
            return None
        else:
            return sa


    def put(self, title, username, ticker):
        s = Survey(title=(AnalysisAPI.get(title)), username=(AnalystAPI.get(username)), ticker=(StockAPI.get(ticker)))
        s.save()

    def remove(self, primary_key):
        sa = Stock_Analysis.objects.get(pk=primary_key)
        sa.delete()

    def getAll(self):
        sa = Stock_Analysis.objects.getAll()
        return sa


class AnalysisAPI:
    def get(self, primary_key):
        try:
            a = Analysis.objects.get(pk=primary_key)
        except(KeyError, Analysis.DoesNotExist):
            return None
        else:
            return a


    def put(self, description, approval, date, title, username):
        a = Analysis(description=description, approval=approval, date=date, title=title, username=(AnalystAPI.get(username)))
        a.save()

    def remove(self, primary_key):
        a = Analysis.objects.get(pk=primary_key)
        a.delete()

    def getAll(self):
        a = Analysis.objects.getAll()
        return a


class AnalystAPI:
    def get(self, primary_key):
        try:
            a = Analyst.objects.get(pk=primary_key)
        except(KeyError, Analyst.DoesNotExist):
            return None
        else:
            return a


    def put(self, username, email, name, password):
        s = Analyst(username=username, email=email, name=name, password=password)
        s.save()

    def remove(self, primary_key):
        a = Analyst.objects.get(pk=primary_key)
        a.delete()

    def getAll(self):
        a = Analyst.objects.getAll()
        return a


class Watchlist_Entry:
    def get(self, primary_key):
        try:
            we = Watchlist_Entry.objects.get(pk=primary_key)
        except(KeyError, Watchlist_Entry.DoesNotExist):
            return None
        else:
            return we


    def put(self, username, ticker):
        we = Watchlist_Entry(username=(UserAPI.get(username)), ticker=(StockAPI.get(ticker)))
        we.save()

    def remove(self, primary_key):
        we = Watchlist_Entry.objects.get(pk=primary_key)
        we.delete()

    def getAll(self):
        we = Watchlist_Entry.objects.getAll()
        return we


class Viewed_History:
    def get(self, primary_key):
        try:
            vh = Viewed_History.objects.get(pk=primary_key)
        except(KeyError, Viewed_History.DoesNotExist):
            return None
        else:
            return vh

    def put(self, date_viewed, username, ticker):
        vh = Viewed_History(date_viewed=date_viewed, username=(UserAPI.get(username)), ticker=(StockAPI.get(ticker)))
        vh.save()

    def remove(self, primary_key):
        vh = Viewed_History.objects.get(pk=primary_key)
        vh.delete()

    def getAll(self):
        vh = Viewed_History.objects.getAll()
        return vh


class ExchangeAPI:
    def get(self, primary_key):
        try:
            e = Exchange.objects.get(pk=primary_key)
        except(KeyError, Exchange.DoesNotExist):
            return None
        else:
            return e

    def put(self, names, exchange_id):
        e = Exchange(names=names, exchange_id=exchange_id)
        e.save()

    def remove(self, primary_key):
        e = Exchange.objects.get(pk=primary_key)
        e.delete()

    def getAll(self):
        e = Exchange.objects.getAll()
        return e



class StockAPI:
    def get(self, primary_key):
        try:
            the_stock = Stock.objects.get(pk=primary_key)
        except(KeyError, Stock.DoesNotExist):
            return None
        else:
            return the_stock


    def put(self, name, current_value, ticker, dividend_date, dividend_ammount, exhange_id):
        s = Stock(name = name, current_value = current_value, ticker = ticker, dividend_date = dividend_date, dividend_ammount = dividend_ammount, exhange_id = ExchangeAPI.get(exhange_id))
        s.save()


    def remove(self, primary_key):
        the_stock = Stock.objects.get(pk=primary_key)
        the_stock.delete()


    def getAll(self):
        u = Stock.objects.getAll()
        return u

class PutAPI:
    def get(self, primary_key):
        try:
            the_put = Put.Objects.get(pk=primary_key)
        except(KeyError, Put.DoesNotExist):
            return None
        else:
            return the_put


    def put(self, expiry_date, strike_price, bid, ask, premium, ticker):
        p = Put(expiry_date = expiry_date, strike_price = strike_price, bid = bid, ask = ask, premium = premium, ticker= StockAPI.get(ticker))
        p.save();


    def remove(self, primary_key):
        the_put = Put.objects.get(pk=primary_key)
        the_put.delete()


    def getAll(self):
        u = Put.objects.getAll()
        return u


class CallAPI:
    def get(self, primary_key):
        try:
            the_call = Call.Objects.get(pk=primary_key)
        except(KeyError, Call.DoesNotExist):
            return None
        else:
            return the_call


    def put(self, expiry_date, strike_price, bid, ask, premium, ticker):
        c = Call(expiry_date = expiry_date, strike_price = strike_price, bid = bid, ask = ask, premium = premium, ticker= StockAPI.get(ticker))
        c.save()


    def remove(self, primary_key):
        the_call = Call.objects.get(pk = primary_key)
        the_call.delete()


    def getAll(self):
        u = Call.objects.getAll()
        return u


class ValueHistoryAPI:
    def get(self, primary_key):
        try:
            the_VHist = Value_History.objects.get(pk=primary_key)
        except(KeyError, Value_History.DoesNotExist):
            return None
        else:
            return the_VHist


    def put(self, id, date, value, ticker):
        vh = Value_History(id = id, date = date, value = value, ticker = StockAPI.get(ticker))
        vh.save()


    def remove(self, primary_key):
        the_VHist = Value_History.objects.get(pk = primary_key)
        the_VHist.delete()


    def getAll(self):
        u = Value_History.objects.getAll()
        return u


class HistogramAPI:
    def get(self, primary_key):
        try:
            the_Histogram = Histogram.object.get(pk = primary_key)
        except(KeyError, Histogram.DoesNotExist):
            return None
        else:
            return the_Histogram


    def put(self, median, quartiles, id):
        h = Histogram(median = median, quartiles = quartiles, id = id)
        h.save()


    def remove(self, primary_key):
        the_Histogram = Histogram.object.get(pk = primary_key)
        the_Histogram.delete()


    def getAll(self):
        u = Histogram.objects.getAll()
        return u