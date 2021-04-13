"""stock_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
# this is a correct import of the views from test app, ignore IDE warnings
from test_app import views

app_name = 'test_app'
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_page),
    path('login_attempt', views.login_attempt, name='login_attempt'),
    path('register_user', views.register_user, name='register_user'),
    path('register_user_attempt', views.register_user_attempt, name='register_user_attempt'),
    path('register_analyst', views.register_analyst, name='register_analyst'),
    path('register_analyst_attempt', views.register_analyst_attempt, name='register_analyst_attempt'),
    path('<str:username>/searching_ticker', views.searching_ticker, name='searching_ticker'),
    path('<str:username>/<str:ticker>/stock_info/', views.view_selected_stock, name='view_selected_stock'),
    path('<str:username>/<str:ticker>/processing_add', views.add_to_watchlist, name='add_to_watchlist'),
    path('add_to_watchlist/', views.add_to_watchlist, name='add_to_watchlist'),
    path('<str:username>/viewed_history/', views.display_viewed_history, name='viewed_history'),
    path('<str:username>/main_page/', views.main_page, name='main_page'),
    path('<str:username>/analyst_main_page', views.analyst_main_page, name='analyst_main_page'),
    path('<str:ticker>/calls_information/', views.calls_information, name='calls_information'),
    path('<str:ticker>/puts_information/', views.puts_information, name='puts_information'),
    path('<str:ticker>/display_calls_information', views.display_calls_information, name='display_calls_information'),
    path('<str:username>/watchlist', views.display_watchlist, name='watchlist')
]
