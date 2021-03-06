

# Create your views here.

from __future__ import unicode_literals
from django.conf import settings
from django.shortcuts import render
from decimal import *

import json
import smtplib
import base64
import os
import pandas as pd
import requests
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

from django.conf import settings

DATA = settings.BASE_DIR

def find_incommings(df_user):
    
    # segment into months
    df_user['year'] = pd.DatetimeIndex(df_user['dates']).year
    df_user['month'] = pd.DatetimeIndex(df_user['dates']).month
    
    # find average income per month
    df_in = df_user[df_user['amount']>0]
    other_account_name = df_in['other_account_name'].unique()
    
    # find average gap in payments
    incomings = {}
    for payment in other_account_name:
        
        df_tmp = df_in[df_in['other_account_name']== payment].copy()
        df_tmp.sort_values(by='dates', inplace=True)
        df_tmp.reset_index(inplace=True, drop=True)
        df_tmp['diff_days'] = pd.to_datetime(df_tmp['dates']).diff().dt.days.fillna(0, downcast='infer')
        
        incomings[payment] = {}
        incomings[payment]['freq'] = math.ceil(df_tmp['diff_days'].mean())
        incomings[payment]['amount'] = df_tmp['amount'].mean()
        incomings[payment]['start_date'] = df_tmp['dates'].min()
           
    return incomings


def find_outgoings(df_user):
    
    # segment into months
    df_user['year'] = pd.DatetimeIndex(df_user['dates']).year
    df_user['month'] = pd.DatetimeIndex(df_user['dates']).month
    
    # find average income per month
    df_in = df_user[df_user['amount']<0]
    other_account_name = df_in['other_account_name'].unique()
        
    # find average gap in payments
    outgoings = {}
    for payment in other_account_name:
        
        df_tmp = df_in[df_in['other_account_name']== payment].copy()
        df_tmp.sort_values(by='dates', inplace=True)
        df_tmp.reset_index(inplace=True, drop=True)
        df_tmp['diff_days'] = pd.to_datetime(df_tmp['dates']).diff().dt.days.fillna(0, downcast='infer')
        
        outgoings[payment] = {}
        outgoings[payment]['freq'] = math.ceil(df_tmp['diff_days'].mean())
        outgoings[payment]['amount'] = df_tmp['amount'].mean()
        outgoings[payment]['start_date'] = df_tmp['dates'].min()
        
        if outgoings[payment]['freq'] > 25:
            outgoings[payment]['Type'] = 'Regular'
        
        if (outgoings[payment]['freq'] >= 7) & (outgoings[payment]['freq'] < 25):
            outgoings[payment]['Type'] = 'Irregular'
            
        if outgoings[payment]['freq'] < 7:
            outgoings[payment]['Type'] = 'Discretionary'
           
    return outgoings


def build_predicted_in_out(user, incommings, outgoings, end_date):
    
    
    in_list = []
    for i in incommings.keys():    
            
        df = pd.DataFrame(data={'dates': pd.date_range(incommings[i]['start_date'], end_date, freq='MS')})
        df['amount_in'] = incommings[i]['amount']
        in_list.append(df)
    
    out_list = []
    for i in outgoings.keys(): 
        
        if outgoings[i]['Type'] == 'Regular':
        
            df = pd.DataFrame(data={'dates': pd.date_range(outgoings[i]['start_date'], end_date, freq=str(outgoings[i]['freq'])+'D')})
            df['amount_out_reg'] = outgoings[i]['amount']
            out_list.append(df)            
        
    df = pd.concat(in_list + out_list)
    df.reset_index(inplace=True,drop=True)
    df.sort_values(by='dates', inplace=True)
    df.reset_index(inplace=True, drop=True)
    df.fillna(0, inplace=True)

    # bucket into months
    df['year'] = pd.DatetimeIndex(df['dates']).year
    df['month'] = pd.DatetimeIndex(df['dates']).month
    
    return df

def gt_buffer(row):
    amount = row['amount']
    buffer = row['buffer']
    txn_type = row['Type']
    other_account_name = row['other_account_name']
    
    alert_flag = False
    if txn_type != 'Regular':
        if abs(amount) > abs(buffer):
            #print('Payment of {} to {} exceeds the projected buffer between regular incoming and outgoing payments this month - are you sure?')
            #alert_dict.update({other_account_name, amount, buffer})
            alert_flag = True
            
    return alert_flag
    

def reg_pay_id(df):
    """
    Returns dict showing regular creditors along with average gaps between payments and average amounts.
    Can be used to generate suggestions for auto-saving pots of money for specific purposes.
    """
    df['dates'] = pd.to_datetime(df['dates'])
        
    df = df.reset_index()    
    main_dict = {}
    for party in list(df['other_account_name'].value_counts().index):
        temp_df = df[df['other_account_name'] == party].copy()
        temp_df['time_since_last_trans_party'] = temp_df['dates'] - temp_df['dates'].shift()        
        temp_df = temp_df.reset_index()
        pos_dict = pd.Series(temp_df['time_since_last_trans_party'].values, index = temp_df['index'])
        main_dict.update(pos_dict)
    df['time_since_last_trans_party'] = df['index'].map(main_dict)    
    
    # Select only Regular payments - can be changed to use cluster tag
    df_reg = df.loc[df['Type'] == 'Regular']
    parties = df_reg['other_account_name'].unique()
    reg_dict = {}
    for party in parties:    
        df_p = df_reg.loc[df_reg['other_account_name'] == party]
        gaps = list(df_p['time_since_last_trans_party'].value_counts().index)                
        if len(gaps) > 0:
            gaps = [x.days for x in gaps if len(gaps) > 0]           
            avg_gap = int(sum(gaps)/len(gaps))        
        else:
            avg_gap = None
        
        amounts = list(df_p['amount'].value_counts().index)  
        amounts = [float(x) for x in amounts]
        avg_amount = sum(amounts)/len(amounts)        
        
        reg_dict.update({party:[avg_gap,round(avg_amount,2)]})
        
    return reg_dict


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
    #with open("data/mock/classify.json", 'r') as fp:
    #    data = json.load(fp)
    df = pd.read_csv('gs://shakingshamrocks_eu/test_data_3_sec.csv')
    df = df.drop(df.columns[0],axis = 1)
    #df_test = df.loc[df['account_name'] == 'Katherine Valencia']
    user_profile = UserProfile.objects.get(user=request.user)

    df_test = df.loc[df['account_name'] == user_profile.account_name]
    json_data = df_test.to_json()
    r = requests.post('https://demo-app-lquvhriy2a-ew.a.run.app/service/classify_v2/',  json= {"data":json_data})
    df_results = pd.read_json(r.json())

    data = df_results
    repay_data = json.dumps(reg_pay_id(df))

    json_data = df.to_json()
    r = requests.post('https://demo-app-lquvhriy2a-ew.a.run.app/service/intelligent/saving_v2/',  json= {"data":json_data})
    saving = r.json()

    context = {'data': json.dumps(data), 'repay_data': repay_data, 'saving':saving}
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

