from django.shortcuts import render
from django.http import HttpResponse
from django.db import models


import datetime

# Create your views here.
def test_view(request):
    now = datetime.datetime.now()
    html = '''
    <html>
      <head>
        <title>
          Connecting to the model
        </title>
      </head>
      <body>
        <h1>
          Connecting to the model
        </h1>
        Only user: %s
      </body>
    </html>''' % (
        'user database acces goes here'
    )
    return HttpResponse(html)