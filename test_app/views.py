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
from test_app.StockDataHolders import *
import plotly.graph_objects as go


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


def main_page(request):
    return render(request, 'test_app/main_page.html', {
        'username': request.session['username'],
        'error_message': ''
    })


def analyst_main_page(request):
    return render(request, 'test_app/analyst_main_page.html', {
        'Username': request.session['username'],
        'error_message': ''
    })


def searching_ticker(request):
    selected_ticker = StockAPI.get(request.POST['ticker'])
    if selected_ticker is None:
        addNewStock(request.POST['ticker'])
        selected_ticker = StockAPI.get(request.POST['ticker'])
    else:
        pullNewStockPrice(selected_ticker.ticker)
    return HttpResponseRedirect(reverse('view_selected_stock', args=(selected_ticker.ticker,)))


def view_selected_stock(request, ticker):
    selected_ticker = StockAPI.get(ticker)
    cv = selected_ticker.current_value
    return render(request, 'test_app/stock_info.html', {
        'ticker': selected_ticker.ticker,
        'value': cv,
        'error_message': "",
    })


def add_to_watchlist(request, ticker):
    selected_ticker = StockAPI.get(ticker)
    error_message = ''
    if WatchlistEntryAPI.get(ticker, request.session['username']) is None:
        WatchlistEntryAPI.put(request.session['username'], ticker)
    else:
        error_message = 'Already On Watchlist'
    return render(request, 'test_app/stock_info.html', {
        'ticker': selected_ticker.ticker,
        'value': selected_ticker.current_value,
        'error_message': error_message,
        'username': request.session['username'],
    })


def calls_information(request, ticker):
    i = 0
    valid_options = 0
    while i < 7:
        the_date = datetime.date.today() + datetime.timedelta(days=i)
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
            'value': StockAPI.get(ticker).current_value,
            'error_message': "There Are No Calls For The Selected Stock"
            })


def display_calls_information(request, ticker):
    call_list = []
    i = 0
    while i < 7:
        the_date = datetime.date.today() + datetime.timedelta(days=i)
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


def display_viewed_history(request, username):
    return render(request, 'test_app/viewed_history.html', {
        'username': username
    })


def puts_information(request, ticker):
    i = 0
    valid_options = 0
    while i < 7:
        the_date = datetime.date.today() + datetime.timedelta(days=i)
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
            'value': StockAPI.get(ticker).current_value,
            'error_message': "There Are No Puts For The Selected Stock"
        })


def display_puts_information(request, ticker):
    put_list = []
    i = 0
    while i < 7:
        the_date = datetime.date.today() + datetime.timedelta(days=i)
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
