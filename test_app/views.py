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

import datetime

# Create your views here.
def login_page(request):
    temp = loader.get_template('test_app/loginPage.html')
    context = {
        'error_message': ''
    }
    return HttpResponse(temp.render(context, request))

def main_page(request):
    try:
        the_user = User.objects.get(pk=request.POST['username'])
    except (KeyError, User.DoesNotExist):
        user_list = User.objects.all()
        for u in user_list:
            print(u.username)
            print(u.password)
        return render(request, 'test_app/loginPage.html', {
            'error_message': 'Incorrect Username'
        })
    else:
        if the_user.password != request.POST['password']:
            return render(request, 'test_app/loginPage.html', {
                'error_message': 'Incorrect Password'
            })
        else:
            return render(request, 'test_app/main_page.html', {
                'error_message': ''
            })


def view_selected_stock(request):
    try:
        selected_ticker = Stock.objects.get(pk=request.POST['ticker'])
    except (KeyError, Stock.DoesNotExist):
        addNewStock(request.POST['ticker'])
        selected_ticker = Stock.objects.get(pk=request.POST['ticker'])
    else:
        pullNewStockPrice(selected_ticker.ticker)
    finally:
        reverse('calls_information', args=(selected_ticker.ticker,))
        return render(request, 'test_app/stock_info.html', {
            'ticker': selected_ticker.ticker,
            'value': selected_ticker.current_value,
            'error_message': ""
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


def display_calls_information(request, ticker):
    return render(request, 'test_app/calls_info.html', {
        'ticker': ticker
    })


def puts_information(request, ticker):
    print()


def test_view(request):
        now = datetime.datetime.now()
        template = loader.get_template('test_app/testStock.html')
        return render(template.render(request))
    #     Only user: %s
    #   </body>
    # </html>''' % (
    #     User.objects.get(username='sample user').name
    # )