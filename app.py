from flask import Flask
import json

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
