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
    return render_template('realtime.html', symbol=symbol)

@app.route('/historical/<symbol>')
def historical(symbol=None):
    return render_template('historical.html', symbol=symbol)

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    name = {1: 'foo', 2: 'bar', 3: 'baz'}
    return render_template('hello.html', name=name)

def main():
    app.run()

if __name__ == '__main__':
    main()
