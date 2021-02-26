

# Create your views here.

from __future__ import unicode_literals
from django.conf import settings
from django.shortcuts import render
from decimal import *

import json
import smtplib
import base64
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import get_list_or_404, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.template import Context, loader
from django.views.generic import TemplateView
from datetime import date, datetime

from calendar import monthrange
from .models import UserProfile
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from django.db.models import Sum


@login_required
def home(request):
    context = {}
    user_profile = UserProfile.objects.get(user=request.user)
    current_date = datetime.now()
    month, year, day = current_date.strftime("%m"), current_date.now().strftime("%Y"), current_date.now().strftime("%d")
    min_amt = user_profile.credit_balance
 
    context.update({'user_profile': user_profile})
    return render(request, 'index.html', context)

def about_us(request):
    context = {}
    return render(request, 'about_us.html', context)

def contact_us(request):
    context = {}
    return render(request, 'contact_us.html', context)


@login_required
def accounts(request):
    context = {}
    return render(request, 'accounts.html', context)

@login_required
def transactions(request):
    with open("./data/mock/transactions_rules.json", 'r') as fp:
        data = json.load(fp)


    context = {'data': json.dumps(data)}
    return render(request, 'transactions.html', context)

@login_required
def alerts(request):
    context = {}
    return render(request, 'alerts.html', context)
  

@login_required
def classify(request):
    with open("data/mock/classify.json", 'r') as fp:
        data = json.load(fp)

    context = {'data': json.dumps(data)}
    return render(request, 'classify.html', context)    

@login_required
def forecast(request):
    with open("data/mock/forecast.json", 'r') as fp:
        data = json.load(fp)
    
    context = {'data': json.dumps(data)}
    return render(request, 'forecast.html', context) 

@login_required
def saving(request):
    with open("./data/mock/intelligent_saving.json", 'r') as fp:
        data = json.load(fp)

    
    context = {'data': json.dumps(data)}
    return render(request, 'savings.html', context) 

@login_required
def service_transactions(request):
    with open("./data/mock/transactions_rules.json", 'r') as fp:
        data = json.load(fp)


    context = {'data': json.dumps(data)}
    
    return render(request, 'service_transactions.html', context) 

@login_required
def rules(request):
    with open("./data/mock/transactions_rules.json", 'r') as fp:
        data = json.load(fp)

    
    context = {'data': json.dumps(data)}
    return render(request, 'rules.html', context) 

