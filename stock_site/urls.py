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
    path('stock_info/', views.view_selected_stock, name='view_selected_stock'),
    path('main_page/', views.main_page, name='main_page'),
    path('<str:ticker>/calls_information/', views.calls_information, name='calls_information'),
    path('<str:ticker>/puts_information/', views.puts_information, name='puts_information'),
    path('<str:ticker>/display_calls_information', views.display_calls_information, name='display_calls_information')
]
