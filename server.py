import json
import random
import time

from flask import Flask, render_template, request
app = Flask(__name__)
app.debug = True

import db
import Future_Predict
from data.historical import insert_data

@app.route('/')
def index():
    stocks_latest = db.get_stocks_realtime()
    return render_template('index.html', stocks=stocks_latest)

@app.route('/realtime/<symbol>')
def realtime(symbol=None):
    name = db.get_name(symbol)[0][0]

    return render_template(
            'realtime.html', 
            symbol=symbol, 
            name=name)

@app.route('/historical/<symbol>')
def historical(symbol=None):
    name = db.get_name(symbol)[0][0]

    return render_template(
            'historical.html', 
            symbol=symbol, 
            name=name)

@app.route('/add')
def add(symbol=None):
    return render_template('add.html')

# This is the callback when the user clicks on sumbit
@app.route('/add_stock')
def add_stock():
    symbol = request.args.get('symbol')
    name = request.args.get('name')

    db.insert_stock(symbol, name)
    insert_data(symbol, 'data/')

    # add model training function here

    return "Stock added and model trained."

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    name = {1: 'foo', 2: 'bar', 3: 'baz'}
    return render_template('hello.html', name=name)

# Ajax endpoints
@app.route('/data/historical_graph/<symbol>')
def data_historical_graph(symbol = None):
    rows = db.get_historical_records(symbol)
    pStock = Future_Predict.predictStock(symbol, "2017-04-24", "hist")
    print len(pStock)
    cleaned = []
    for row in rows:
        # print row[1], row[5]
        temp = {}
        temp["date"] = row[1]
        temp["closePrice"]  = row[5]
        # temp["pred"] = row[5] + random.randint(-2, 2)
        cleaned.append(temp)

    lastdate1 = time.strptime(cleaned[len(cleaned)-1]["date"], "%Y-%m-%d")
    for dic in pStock:
        newdate1 = time.strptime(dic["date"], "%Y-%m-%d")
        if lastdate1 < newdate1:
            temp = {}
            temp["date"] = dic["date"]
            # temp["closePrice"] = 50
            temp["pred"] = dic["prediction"]
            temp["ci_up"] = 0
            temp["ci_down"] = 0
            cleaned.append(temp)
        else:
            for c in cleaned:
                if c["date"] == dic["date"]:
                    c["pred"] = dic["prediction"]
                    # print c["pred"], dic["prediction"]

    # print cleaned[-24:]
    return json.dumps(cleaned)

@app.route('/data/realtime_graph/<symbol>')
def data_realtime_graph(symbol = None):
    rows = db.get_realtime_records(symbol)
    cleaned = []
    for row in rows:
        temp = {}
        temp["date"] = row[1] + ' ' + row[2]
        temp["price"]  = row[3]
        # temp["pred"] = row[5] + random.randint(-2, 2)
        cleaned.append(temp)

    return json.dumps(cleaned)

@app.route('/data/highlow/<symbol>')
def highlow(symbol=None):
    high_10 = db.get_highest_ten_days(symbol)[0]
    avg_1_year = db.get_average_one_year(symbol)[0][0]
    low_1_year = db.get_lowest_one_year(symbol)[0]

    return render_template(
            'high_low.html', 
            high_10=high_10,
            avg_1_year=avg_1_year,
            low_1_year=low_1_year)

@app.route('/data/avglow/<symbol>')
def avglow(symbol=None):
    avg_low = db.get_avg_low(symbol)
    return render_template(
            'avg_low.html',
            avg_low=avg_low)

def main():
    app.run()

if __name__ == '__main__':
    main()
