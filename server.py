from flask import Flask, render_template
app = Flask(__name__)
app.debug = True

import db

@app.route('/')
def index():
    stocks_latest = db.get_stocks_realtime()
    return render_template('index.html', stocks=stocks_latest)

@app.route('/realtime/<symbol>')
def realtime(symbol=None):
    high_10 = db.get_highest_ten_days(symbol)
    avg_1_year = db.get_average_one_year(symbol)
    low_1_year = db.get_lowest_one_year(symbol)
    avg_low = db.get_avg_low(symbol)
    return render_template(
            'realtime.html', 
            symbol=symbol, 
            high_10=high_10,
            avg_1_year=avg_1_year,
            low_1_year=low_1_year,
            avg_low=avg_low)

@app.route('/historical/<symbol>')
def historical(symbol=None):
    high_10 = db.get_highest_ten_days(symbol)
    avg_1_year = db.get_average_one_year(symbol)
    low_1_year = db.get_lowest_one_year(symbol)
    avg_low = db.get_avg_low(symbol)
    return render_template(
            'historical.html', 
            symbol=symbol, 
            high_10=high_10,
            avg_1_year=avg_1_year,
            low_1_year=low_1_year,
            avg_low=avg_low)

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    name = {1: 'foo', 2: 'bar', 3: 'baz'}
    return render_template('hello.html', name=name)

def main():
    app.run()

if __name__ == '__main__':
    main()
