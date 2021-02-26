import pandas as pd
import math

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


def forecasting(df):
    # Will be called on a per user basis
    incommings_payments = find_incommings(df.copy())
    outgoing_payments = find_outgoings(df.copy())
    
    # Should be only one user in df
    account_name = list(df['account_name'].value_counts().index)[0]
    
    df_tmp = build_predicted_in_out(account_name, incommings_payments, outgoing_payments, '2024-01-01 00:00:00')
    
    gf_payment_pattern_reg = df_tmp.groupby(['year','month'])[['amount_in','amount_out_reg']].sum()
    gf_payment_pattern_reg['buffer'] = gf_payment_pattern_reg['amount_in'] + gf_payment_pattern_reg['amount_out_reg']
    
    # Make Year and Month columns in df, for use as join keys
    df['year'] = df['dates'].apply(lambda x: int(x[:4]))
    df['month'] = df['dates'].apply(lambda x: int(x[5:7]))
    
    # Promote multi-index
    gf_payment_pattern_reg = gf_payment_pattern_reg.reset_index()
    
    df_join = pd.merge(df,gf_payment_pattern_reg, how = 'left', on = ['year','month'])
    
    df_join['buffer_alert'] = df_join.apply(gt_buffer, axis = 1)
    print(df_join.head())
    print(df_join.to_json())
    
    df_json = df_join.to_json()
        
    return df_json
    
    
    
    
    
    
    
    
    
    
    
    
    