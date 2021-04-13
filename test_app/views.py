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
import datetime
import plotly.graph_objects as go

# Create your views here.
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
            return HttpResponseRedirect(reverse('main_page', args=(the_user.username,)))
        else:
            return HttpResponseRedirect(reverse('analyst_main_page', args=(the_analyst.username,)))


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

def main_page(request, username):
    return render(request, 'test_app/main_page.html', {
        'username': username,
        'error_message': ''
    })

def analyst_main_page(request, username):
    return render(request, 'test_app/analyst_main_page.html', {
        'Username': username,
        'error_message': ''
    })


def searching_ticker(request, username):
    selected_ticker = StockAPI.get(request.POST['ticker'])
    if selected_ticker is None:
        addNewStock(request.POST['ticker'])
        selected_ticker = StockAPI.get(request.POST['ticker'])
    else:
        pullNewStockPrice(selected_ticker.ticker)
    return HttpResponseRedirect(reverse('view_selected_stock', args=(username, selected_ticker.ticker,)))


def view_selected_stock(request, username, ticker):
    selected_ticker = StockAPI.get(ticker)
    cv = selected_ticker.current_value
    return render(request, 'test_app/stock_info.html', {
        'ticker': selected_ticker.ticker,
        'value': cv,
        'error_message': "",
        'username': username,
    })

def add_to_watchlist(request, username, ticker):
    selected_ticker = StockAPI.get(ticker)
    current_user = StockAPI.get(username)
    error_message = ''
    if WatchlistEntryAPI.get(ticker, username) is None:
        WatchlistEntryAPI.put(username, ticker)
    else:
        error_message = 'Already On Watchlist'
    return render(request, 'test_app/stock_info.html', {
        'ticker': selected_ticker.ticker,
        'value': selected_ticker.current_value,
        'error_message': error_message,
        'username': username,
    })


def calls_information(request, ticker):
    try:
        selected_ticker = Stock.objects.get(pk=ticker)
    except (KeyError, Stock.DoesNotExist):
        return render(request, 'test_app/stock_info.html', {
            'ticker': selected_ticker.ticker,
            'value': selected_ticker.current_value,
            'error_message': "Database Error"
        })
    else:
        try:
            calls = Call.objects.filter(ticker=selected_ticker)
        except (KeyError, Call.DoesNotExist):
            calls_exist = addCalls(ticker)
            if calls_exist:
                calls = Call.objects.filter(ticker=selected_ticker)
                return HttpResponseRedirect(reverse('display_calls_information', args=(ticker,)))
            else:
                return render(request, 'test_app/stock_info.html', {
                    'ticker': selected_ticker.ticker,
                    'value': selected_ticker.current_value,
                    'error_message': "There Are No Calls For The Selected Stock"
                })
        else:
            return HttpResponseRedirect(reverse('display_calls_information', args=(ticker,)))

def display_watchlist(request, username):
    watchlist = WatchlistEntryAPI.get_for_user(username)
    return render(request, 'test_app/watchlist.html', {
        'username': username,
        'watchlist': watchlist
    })

def display_viewed_history(request, username):
    return render(request, 'test_app/viewed_history.html', {
        'username': username
    })

def display_calls_information(request, ticker):
    return render(request, 'test_app/calls_info.html', {
        'ticker': ticker
    })


def puts_information(request, ticker):
    return render(request, 'test_app/puts_info.html', {
        'ticker': ticker
    })


def test_view(request):
        now = datetime.datetime.now()
        template = loader.get_template('test_app/testStock.html')
        return render(template.render(request))
    #     Only user: %s
    #   </body>
    # </html>''' % (
    #     User.objects.get(username='sample user').name
    # )