from django.shortcuts import render
from django.http import HttpResponse
from django.db import models
from django.views.generic import *
from test_app.models import *

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
        User.objects.get(username='sample user').name
    )
    return HttpResponse(html)