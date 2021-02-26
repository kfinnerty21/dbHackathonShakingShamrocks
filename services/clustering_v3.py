from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.cluster import DBSCAN
import pandas as pd



def convert_to_mins_v3(val):
    try:
        return(int((val.total_seconds()/60)))
    except ValueError:
        return np.nan

def cluster_analysis_v3(df_test):
    df_test['datetime'] = df_test['dates'].apply(lambda x: datetime.datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))
    df_test['time_since_last_transaction'] = df_test['datetime'] - df['datetime'].shift()
    df_test['time_since_last_transaction']= df_test['time_since_last_transaction'].apply(lambda x: convert_to_mins(x))
    df_test = df_test.reset_index()
    
    main_dict = {}
    for party in list(df_test['other_account_name'].value_counts().index):
        temp_df = df_test[df_test['other_account_name'] == party].copy()
        temp_df['time_since_last_trans_party'] = temp_df['datetime'] - temp_df['datetime'].shift()
        pos_dict = pd.Series(temp_df['time_since_last_trans_party'].values, index = temp_df['index'])
        main_dict.update(pos_dict)
    df_test['time_since_last_transaction_party'] = df_test['index'].map(main_dict)
    df_test['time_since_last_transaction_party']= df_test['time_since_last_transaction_party'].apply(lambda x: convert_to_mins(x))
    
    
    numeric_features = ['amount', 'day', 'time_since_last_transaction_party', 'time_since_last_transaction']
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())])
    # account name used as dummy feature
    categorical_features = ['account_name']
    categorical_transformer = OneHotEncoder(handle_unknown='ignore')

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)])

    clf = Pipeline(steps=[('preprocessor', preprocessor),
                          ('cluster', DBSCAN(0.2))])

    df_test.dates = pd.to_datetime(df_test.dates)
    df_test['day'] = df_test.dates.dt.day
    df_test.head()
    #df = df[[]]
    prediction = clf.fit_predict(df_test)

    df_test['prediction'] = "Regular-Irregular"
    df_test.loc[prediction < 0, 'prediction'] = 'Discretionary'

    return df_test