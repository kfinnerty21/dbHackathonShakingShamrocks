from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.cluster import DBSCAN
import pandas as pd


def cluster_analysis(df_test):
    numeric_features = ['amount', 'day']
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

    prediction = clf.fit_predict(df_test)

    df_test['prediction'] = "Regular-Irregular"
    df_test.loc[prediction < 0, 'prediction'] = 'Discretionary'

    return df_test
