import pandas as pd

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
        pos_dict = pd.Series(temp_df['time_since_last_trans_party'].values, index=temp_df['index'])
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
            avg_gap = int(sum(gaps) / len(gaps))
        else:
            avg_gap = None

        amounts = list(df_p['amount'].value_counts().index)
        amounts = [float(x) for x in amounts]
        avg_amount = sum(amounts) / len(amounts)

        reg_dict.update({party: [avg_gap, round(avg_amount, 2)]})

    return reg_dict