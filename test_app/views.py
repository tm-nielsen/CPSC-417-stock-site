from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context
from django.shortcuts import render
from django.db import models
from django.views.generic import *
from test_app.models import *
import yfinance as yf
from django.urls import reverse
from test_app.stockDataCollector import *
from .models import Stock, User, Call, Put
from test_app.API import *
from datetime import datetime, date, timedelta
from test_app.StockDataHolders import *
import pandas as pd
from django.db.models import Sum
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.serializers import Serializer
from .models import *
from .serializer import *


class User_(APIView):
    def get(self, request, pk, format=None):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user, data=request.data)
        print(user)
        if serializer.is_valid():
            print(request.data)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = User.objects.filter(pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class User__(APIView):

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data)

class Analyst_(APIView):
    def get(self, request, pk, format=None):
        a = Analyst.objects.get(pk=pk)
        serializer = AnalystSerializer(a)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        a = Analyst.objects.get(pk=pk)
        serializer = AnalystSerializer(a, data=request.data)
        print(a)
        if serializer.is_valid():
            print(request.data)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        a = Analyst.objects.filter(pk=pk)
        a.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Analyst__(APIView):

    def post(self, request, format=None):
        serializer = AnalystSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        analyst = Analyst.objects.all()
        serializer = AnalystSerializer(analyst,many=True)
        return Response(serializer.data)


class Analysis_(APIView):
    def get(self, request, title, username, format=None):
        a = Analysis.objects.get(title=title, username=Analyst.objects.get(pk=username))
        serializer = AnalysisSerializer(a)
        return Response(serializer.data)

    def put(self, request, title, username, format=None):
        a = Analysis.objects.get(title=title, username=Analyst.objects.get(pk=username))
        serializer = AnalysisSerializer(a, data=request.data)
        print(a)
        if serializer.is_valid():
            print(request.data)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, title, username, format=None):
        a = Analysis.objects.filter(title=title, username=Analyst.objects.get(pk=username))
        a.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Analysis__(APIView):

    def post(self, request, format=None):
        serializer = AnalysisSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        analysis = Analysis.objects.all()
        serializer = AnalysisSerializer(analysis,many=True)
        return Response(serializer.data)


class Exchange_(APIView):
    def get(self, request, pk, format=None):
        e = Exchange.objects.get(pk=pk)
        serializer = ExchangeSerializer(e)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        e = Exchange.objects.get(pk=pk)
        serializer = ExchangeSerializer(e, data=request.data)
        print(e)
        if serializer.is_valid():
            print(request.data)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        e = Exchange.objects.filter(pk=pk)
        e.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Exchange__(APIView):

    def post(self, request, format=None):
        serializer = ExchangeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        exchange = Exchange.objects.all()
        serializer = ExchangeSerializer(exchange,many=True)
        return Response(serializer.data)

class Stock_(APIView):
    def get(self, request, pk, format=None):
        s = Stock.objects.get(pk=pk)
        serializer = StockSerializer(s)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        s = Stock.objects.get(pk=pk)
        serializer = StockSerializer(s, data=request.data)
        print(s)
        if serializer.is_valid():
            print(request.data)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        s = Stock.objects.filter(pk=pk)
        s.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Stock__(APIView):

    def post(self, request, format=None):
        serializer = StockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        stock = Stock.objects.all()
        serializer = StockSerializer(stock,many=True)
        return Response(serializer.data)


class Put_(APIView):
    def get(self, request, ed, sp, t, format=None):
        p = Put.objects.get(expiry_date=ed, strike_price=float(sp), ticker=Stock.objects.get(pk=t))
        serializer = PutSerializer(p)
        return Response(serializer.data)

    def put(self, request, ed, sp, t, format=None):
        p = Put.objects.get(expiry_date=ed, strike_price=float(sp), ticker=Stock.objects.get(pk=t))
        serializer = PutSerializer(p, data=request.data)
        print(p)
        if serializer.is_valid():
            print(request.data)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, ed, sp, t, format=None):
        p = Put.objects.filter(expiry_date=ed, strike_price=float(sp), ticker=Stock.objects.get(pk=t))
        p.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Put__(APIView):

    def post(self, request, format=None):
        serializer = PutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        put = Put.objects.all()
        serializer = PutSerializer(put,many=True)
        return Response(serializer.data)


class Call_(APIView):
    def get(self, request, ed, sp, t, format=None):
        c = Call.objects.get(expiry_date=ed, strike_price=float(sp), ticker=Stock.objects.get(pk=t))
        serializer = CallSerializer(c)
        return Response(serializer.data)

    def put(self, request, ed, sp, t, format=None):
        c = Call.objects.get(expiry_date=ed, strike_price=float(sp), ticker=Stock.objects.get(pk=t))
        serializer = CallSerializer(c, data=request.data)
        print(c)
        if serializer.is_valid():
            print(request.data)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, ed, sp, t, format=None):
        c = Call.objects.filter(expiry_date=ed, strike_price=float(sp), ticker=Stock.objects.get(pk=t))
        c.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Call__(APIView):

    def post(self, request, format=None):
        serializer = CallSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        call = Call.objects.all()
        serializer = CallSerializer(call,many=True)
        return Response(serializer.data)


class ValueHistory_(APIView):
    def get(self, request, d, ticker, format=None):
        vh = Value_History.objects.get(date=d, ticker=Stock.objects.get(pk=ticker))
        serializer = ValueHistorySerializer(vh)
        return Response(serializer.data)

    def put(self, request, d, ticker, format=None):
        vh = Value_History.objects.get(date=d, ticker=Stock.objects.get(pk=ticker))
        serializer = ValueHistorySerializer(vh, data=request.data)
        print(vh)
        if serializer.is_valid():
            print(request.data)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, d, ticker, format=None):
        vh = Value_History.objects.filter(date=d, ticker=Stock.objects.get(pk=ticker))
        vh.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ValueHistory__(APIView):

    def post(self, request, format=None):
        serializer = ValueHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        vh = Value_History.objects.all()
        serializer = ValueHistorySerializer(vh,many=True)
        return Response(serializer.data)


class HistogramEntry_(APIView):
    def get(self, request, d, ticker, format=None):
        he = Histogram_Entry.objects.get(id=Value_History.objects.get(date=d, ticker=Stock.objects.get(pk=ticker)))
        serializer = HistogramEntrySerializer(he)
        return Response(serializer.data)

    def put(self, request, d, ticker, format=None):
        he = Histogram_Entry.objects.get(
            id=Value_History.objects.get(date=d, ticker=Stock.objects.get(pk=ticker)))
        serializer = HistogramEntrySerializer(he, data=request.data)
        print(he)
        if serializer.is_valid():
            print(request.data)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, d, ticker, format=None):
        he = Histogram_Entry.objects.filter(id=Value_History.objects.get(date=d, ticker=Stock.objects.get(pk=ticker)))
        he.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class HistogramEntry__(APIView):

    def post(self, request, format=None):
        serializer = HistogramEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        hist = Value_History.objects.all()
        serializer = HistogramEntrySerializer(hist,many=True)
        return Response(serializer.data)


class ViewedHistory_(APIView):
    def get(self, request, d, username, ticker, format=None):
        vh = Viewed_History.objects.get(date_viewed=d, username=User.objects.get(pk=username),
                                       ticker=Stock.objects.get(pk=ticker))
        serializer = ViewedHistorySerializer(vh)
        return Response(serializer.data)

    def put(self, request, d, username, ticker, format=None):
        vh = Viewed_History.objects.get(date_viewed=d, username=User.objects.get(pk=username),
                                          ticker=Stock.objects.get(pk=ticker))
        serializer = ViewedHistorySerializer(vh, data=request.data)
        print(vh)
        if serializer.is_valid():
            print(request.data)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, d, username, ticker, format=None):
        vh = Viewed_History.objects.filter(date_viewed=d, username=User.objects.get(pk=username),
                                          ticker=Stock.objects.get(pk=ticker))
        vh.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ViewedHistory__(APIView):

    def post(self, request, format=None):
        serializer = ViewedHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        viewed = Viewed_History.objects.all()
        serializer = ViewedHistorySerializer(viewed,many=True)
        return Response(serializer.data)


class WatchlistEntry_(APIView):
    def get(self, request, ticker, username, format=None):
        we = Watchlist_Entry.objects.get(ticker=Stock.objects.get(pk=ticker), username=User.objects.get(pk=username))
        serializer = WatchlistEntrySerializer(we)
        return Response(serializer.data)

    def put(self, request, ticker, username, format=None):
        we = Watchlist_Entry.objects.get(ticker=Stock.objects.get(pk=ticker),
                                            username=User.objects.get(pk=username))
        serializer = WatchlistEntrySerializer(we, data=request.data)
        print(we)
        if serializer.is_valid():
            print(request.data)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, ticker, username, format=None):
        we = Watchlist_Entry.objects.filter(ticker=Stock.objects.get(pk=ticker), username=User.objects.get(pk=username))
        we.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WatchlistEntry__(APIView):

    def post(self, request, format=None):
        serializer = WatchlistEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        entry = Watchlist_Entry.objects.all()
        serializer = WatchlistEntrySerializer(entry,many=True)
        return Response(serializer.data)
# ----------------------------------------------------------------------------------------------------------------------

def login_page(request):
    temp = loader.get_template('test_app/loginPage.html')
    context = {
        'message': ''
    }
    return HttpResponse(temp.render(context, request))


def login_attempt(request):
    the_user = UserAPI.get(request.POST['username'])
    the_analyst = AnalystAPI.get(request.POST['username'])
    if the_user is None and the_analyst is None:
        return render(request, 'test_app/loginPage.html', {
            'message': 'Incorrect Username'
        })
    else:
        if (the_user is not None and the_user.password != request.POST['password']) or \
                (the_analyst is not None and the_analyst.password != request.POST['password']):
            return render(request, 'test_app/loginPage.html', {
                'message': 'Incorrect Password'
            })
        elif the_user is not None:
            request.session['username'] = request.POST['username']
            return HttpResponseRedirect('main_page')
        else:
            request.session['username'] = request.POST['username']
            return HttpResponseRedirect(reverse('analyst_main_page'))


def register_user(request):
    return render(request, 'test_app/register_user.html', {
        'error_message': ''
    })


def register_user_attempt(request):
    username = request.POST['username']
    password = request.POST['password']
    name = request.POST['name']
    email = request.POST['email']
    check_dup_user_username = UserAPI.get(username)
    check_dup_analyst_username = AnalystAPI.get(username)
    if check_dup_user_username is not None or check_dup_analyst_username is not None:
        return render(request, 'test_app/register_user.html', {
            'error_message': 'This Username is Taken'
        })
    elif not name or not email or not username or not password:
        return render(request, 'test_app/register_user.html', {
            'error_message': 'Please Fill Out All Required Fields'
        })
    UserAPI.put(username, email, name, password)
    return render(request, 'test_app/loginPage.html', {
        'message': 'Account Created Successfully'
    })


def register_analyst(request):
    return render(request, 'test_app/register_analyst.html', {
        'error_message': ''
    })


def register_analyst_attempt(request):
    username = request.POST['username']
    password = request.POST['password']
    name = request.POST['name']
    email = request.POST['email']
    check_dup_user_username = UserAPI.get(username)
    check_dup_analyst_username = AnalystAPI.get(username)
    if check_dup_user_username is not None or check_dup_analyst_username is not None:
        return render(request, 'test_app/register_analyst.html', {
            'error_message': 'This Username is Taken'
        })
    elif not name or not email or not username or not password:
        return render(request, 'test_app/register_analyst.html', {
            'error_message': 'Please Fill Out All Required Fields'
        })
    AnalystAPI.put(username, email, name, password)
    return render(request, 'test_app/loginPage.html', {
        'message': 'Account Created Successfully'
    })


def main_page(request):
    return render(request, 'test_app/main_page.html', {
        'username': request.session['username'],
        'error_message': ''
    })


def analyst_main_page(request):
    return render(request, 'test_app/analyst_main_page.html', {
        'username': request.session['username'],
        'error_message': ''
    })


def create_analysis(request):
    return render(request, 'test_app/create_analysis.html', {
    })


def save_analysis(request):
    title = request.POST['title']
    description = request.POST['description']
    the_date = date.today()
    username = request.session['username']
    AnalysisAPI.put(description, the_date, title, username)
    request.session['username'] = username
    return HttpResponseRedirect(reverse('analyst_main_page'))


def search_analysis(request):
    selected_analysis = AnalysisAPI.get(request.POST['analysis'])
    if selected_analysis is None:
        return render(request, 'test_app/analyst_main_page.html', {
            'username': request.session['username'],
            'error_message': 'Analysis not found. Please try again'
        })
    else:
        return render(request, 'test_app/view_analysis.html', {
            'title': selected_analysis.title,
            'author': selected_analysis.username.username,
            'date': selected_analysis.date,
            'description': selected_analysis.description
        })


def viewed_history_search(request):
    j = 0
    ticker = ''
    for i in request.POST:
        if j == 1:
            ticker = i
        else:
            j = j + 1
    print(ticker)
    pullNewStockPrice(ticker)
    right_now = datetime.now()
    ViewedHistoryAPI.put(right_now, request.session['username'], ticker)
    return HttpResponseRedirect(reverse('view_selected_stock', args=(ticker,)))


def searching_ticker(request):
    selected_ticker = StockAPI.get(request.POST['ticker'])
    if selected_ticker is None:
        stock_exists = addNewStock(request.POST['ticker'])
        if not stock_exists:
            return render(request, 'test_app/main_page.html', {
                'username': request.session['username'],
                'error_message': 'Unable to Find a Matching Ticker'
            })
        selected_ticker = StockAPI.get(request.POST['ticker'])
        right_now = datetime.now()
        ViewedHistoryAPI.put(right_now, request.session['username'], request.POST['ticker'])
    else:
        pullNewStockPrice(selected_ticker.ticker)
        right_now = datetime.now()
        ViewedHistoryAPI.put(right_now, request.session['username'], request.POST['ticker'])
    return HttpResponseRedirect(reverse('view_selected_stock', args=(selected_ticker.ticker,)))


def user_search_analysis(request):
    selected_analysis = AnalysisAPI.get(request.POST['analysis'])
    if selected_analysis is None:
        return render(request, 'test_app/main_page.html', {
            'username': request.session['username'],
            'error_message': 'Analysis not found. Please try again'
        })
    else:
        return render(request, 'test_app/view_analysis.html', {
            'title': selected_analysis.title,
            'author': selected_analysis.username.username,
            'date': selected_analysis.date,
            'description': selected_analysis.description
        })


def view_selected_stock(request, ticker):
    selected_ticker = StockAPI.get(ticker)
    right_now = datetime.now()
    if ValueHistoryAPI.get(selected_ticker, right_now) is None:
        ValueHistoryAPI.put(right_now, selected_ticker.current_value, ticker)
        new_history = ValueHistoryAPI.get(selected_ticker, right_now)
        Histogram_EntryAPI.put(selected_ticker.current_value, new_history)
    return render(request, 'test_app/stock_info.html', {
        'ticker': selected_ticker.ticker,
        'exchange': StockAPI.get(ticker).exchange_id,
        'stock': selected_ticker,
        'error_message': "",
    })


def add_to_watchlist(request, ticker):
    selected_ticker = StockAPI.get(ticker)
    if WatchlistEntryAPI.get(ticker, request.session['username']) is None:
        WatchlistEntryAPI.put(request.session['username'], ticker)
        error_message = 'Added Successfully'
    else:
        error_message = 'Already On Watchlist'
    return render(request, 'test_app/stock_info.html', {
        'ticker': selected_ticker.ticker,
        'exchange': StockAPI.get(ticker).exchange_id,
        'stock': selected_ticker,
        'error_message': error_message,
        'username': request.session['username'],
    })


def calls_information(request, ticker):
    i = 0
    valid_options = 0
    while i < 7:
        the_date = date.today() + timedelta(days=i)
        days_call = CallAPI.get_expiring_on(ticker, the_date)
        if days_call is None:
            valid = addCalls(ticker, the_date)
            if valid:
                valid_options = valid_options + 1
        else:
            pull_new_calls_info(ticker, the_date)
            valid_options = valid_options + 1
        i += 1
    if valid_options != 0:
        return HttpResponseRedirect(reverse('display_calls_information', args=(ticker,)))
    else:
        return render(request, 'test_app/stock_info.html', {
            'ticker': ticker,
            'exchange': StockAPI.get(ticker).exchange_id,
            'stock': StockAPI.get(ticker),
            'error_message': "There Are No Calls For The Selected Stock"
        })


def display_calls_information(request, ticker):
    call_list = []
    i = 0
    while i < 7:
        the_date = date.today() + timedelta(days=i)
        days_call = CallAPI.get_expiring_on(ticker, the_date)
        if days_call is None:
            i = i + 1
            continue
        else:
            year = the_date.strftime("%Y")
            month = the_date.strftime("%m")
            day = the_date.strftime("%d")
            string_date = year + '-' + month + '-' + day
            cr = CallsResultsHolder(string_date)
            for n in days_call:
                cr.add_call(n)
            call_list.append(cr)
            i = i + 1
    return render(request, 'test_app/calls_info.html', {
        'ticker': ticker,
        'call_list': call_list
    })


def display_watchlist(request):
    watchlist = WatchlistEntryAPI.get_for_user(request.session['username'])
    return render(request, 'test_app/watchlist.html', {
        'watchlist': watchlist
    })


def display_viewed_history(request):
    history_list = ViewedHistoryAPI.get_user_history(request.session['username'])
    results = []
    to_delete = []
    for i in history_list:
        results.append(i)
    j = 0
    for i in results:
        if j > 9:
            to_delete.append(i)
            j = j + 1
        else:
            j = j + 1
    for i in to_delete:
        ViewedHistoryAPI.remove(i)
        results.remove(i)
    return render(request, 'test_app/viewed_history.html', {
        'username': request.session['username'],
        'history_list': results
    })


def puts_information(request, ticker):
    i = 0
    valid_options = 0
    while i < 7:
        the_date = date.today() + timedelta(days=i)
        days_put = PutAPI.get_expiring_on(ticker, the_date)
        if days_put is None:
            valid = addPuts(ticker, the_date)
            if valid:
                valid_options = valid_options + 1
        else:
            pull_new_puts_info(ticker, the_date)
            valid_options = valid_options + 1
        i += 1
    if valid_options != 0:
        return HttpResponseRedirect(reverse('display_puts_information', args=(ticker,)))
    else:
        return render(request, 'test_app/stock_info.html', {
            'ticker': ticker,
            'exchange': StockAPI.get(ticker).exchange_id,
            'stock': StockAPI.get(ticker),
            'error_message': "There Are No Puts For The Selected Stock"
        })


def display_puts_information(request, ticker):
    put_list = []
    i = 0
    while i < 7:
        the_date = date.today() + timedelta(days=i)
        days_put = PutAPI.get_expiring_on(ticker, the_date)
        if days_put is None:
            i = i + 1
            continue
        else:
            year = the_date.strftime("%Y")
            month = the_date.strftime("%m")
            day = the_date.strftime("%d")
            string_date = year + '-' + month + '-' + day
            pr = PutsResultsHolder(string_date)
            for n in days_put:
                pr.add_put(n)
            put_list.append(pr)
            i = i + 1
    return render(request, 'test_app/puts_info.html', {
        'ticker': ticker,
        'put_list': put_list
    })


def display_histogram(request, ticker):
    return render(request, 'test_app/histogram.html', {
        'ticker': ticker
    })


def histogram_chart(request, ticker):
    val_hists = ValueHistoryAPI.all_for_ticker(StockAPI.get(ticker))
    vals = []
    dates = []
    for i in val_hists:
        hist_entry = Histogram_EntryAPI.get(i)
        vals.append(hist_entry.value)
        dates.append(i.date.strftime("%m/%d/%Y, %H:%M:%S"))
    return JsonResponse(data={
        'labels': dates,
        'data': vals,
    })
