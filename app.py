from flask import Flask, request
import json
import pandas as pd
from services.clustering import cluster_analysis
from services.intel_saving import reg_pay_id
from services.forecasting import forecasting
from services.clustering_v3 import cluster_analysis_v3

app = Flask('hello')


@app.route('/')
def hello():
    s = """Hello World!<br>
           Classification service is available on : '/service/classify/' <br>
           Forecasting service is available on : '/service/forecast/'<br>
           Intelligent Saving service is available on : '/service/intelligent/saving/'<br>
           Transaction Rules service is available on : '/service/transactions/rules/'<br>
        """
    return s


@app.route('/service/classify/')
def classify():
    with open("./data/mock/classify.json", 'r') as fp:
        data = json.load(fp)
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/service/classify_v3/', methods=['POST', 'GET'])
def classify_v2():
    data = request.get_json()
    if data['data']:

        df = pd.read_json(data['data'])
        cluster_data = cluster_analysis_v3(df)
        data_return = cluster_data.to_json()
    else:
        data_return = {"Error"}
    response = app.response_class(
        response=json.dumps(data_return),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/service/classify_v2/', methods=['POST', 'GET'])
def classify_v2():
    data = request.get_json()
    if data['data']:

        df = pd.read_json(data['data'])
        cluster_data = cluster_analysis(df)
        data_return = cluster_data.to_json()
    else:
        data_return = {"Error"}
    response = app.response_class(
        response=json.dumps(data_return),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/service/forecast_v2/', methods=['POST', 'GET'])
def forecast_v2():
    data = request.get_json()
    if data['data']:

        df = pd.read_json(data['data'])
        forecast_data = forecasting(df)
        data_return = forecast_data.to_json()
    else:
        data_return = {"Error"}
    response = app.response_class(
        response=json.dumps(data_return),
        status=200,
        mimetype='application/json'
    )
    return response



@app.route('/service/forecast/')
def forecast():
    with open("./data/mock/forecast.json", 'r') as fp:
        data = json.load(fp)
    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/service/intelligent/saving/')
def intelligent_saving():
    with open("./data/mock/intelligent_saving.json", 'r') as fp:
        data = json.load(fp)

    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/service/intelligent/saving_v2/', methods=['POST', 'GET'])
def intelligent_saving_v2():
    data = request.get_json()
    if data['data']:
        df = pd.read_json(data['data'])
        data_result = reg_pay_id(df)
    else:
        data_result = {"Error"}

    response = app.response_class(
        response=json.dumps(data_result),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/service/transactions/rules/')
def transactions_rules():
    with open("./data/mock/transactions_rules.json", 'r') as fp:
        data = json.load(fp)

    response = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
