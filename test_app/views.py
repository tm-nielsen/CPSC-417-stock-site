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

# Create your views here.
def login_page(request):
    temp = loader.get_template('test_app/loginPage.html')
    context = {
        'error_message': ''
    }
    return HttpResponse(temp.render(context, request))

def login_attempt(request):
    the_user = UserAPI.get(request.POST['username'])
    if the_user is None:
        return render(request, 'test_app/loginPage.html', {
            'error_message': 'Incorrect Username'
        })
    else:
        if the_user.password != request.POST['password']:
            return render(request, 'test_app/loginPage.html', {
                'error_message': 'Incorrect Password'
            })
        else:
            return HttpResponseRedirect(reverse('main_page', args=(the_user.username,)))


def register_user(request):
    return render(request, 'test_app/register_user.html')


def register_analyst(request):
    return render(request, 'test_app/register_analyst.html')


def main_page(request, username):
    return render(request, 'test_app/main_page.html', {
        'username': username,
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
    return render(request, 'test_app/stock_info.html', {
        'ticker': selected_ticker.ticker,
        'value': selected_ticker.current_value,
        'error_message': "",
        'username': username
    })

def add_to_watchlist(request, username, ticker):
    selected_ticker = StockAPI.get(ticker)

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
    return render(request, 'test_app/watchlist.html', {
        'username': username
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