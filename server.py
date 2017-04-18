import json
import sqlite3
from flask import Flask, render_template
app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return render_template('index.html')

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

@app.route('/plot/')
@app.route('/plot/<name>')
def plot(name=None):
	conn = sqlite3.connect('data/stocks.db')
	cursor = conn.cursor()

	cursor.execute('SELECT * FROM historical LIMIT 50')
	rows = cursor.fetchall()

	cleaned = []
	ctr = 1

	for row in rows:
	    # print row[4], row[5]
	    temp = {}
	    temp["closePrice"]  = row[4]
	    temp["date"] = row[5]
	    cleaned.append(temp)
	    ctr += 1

	# for row in cleaned:
	    # print row

	conn.close()

	# fp = open('templates/data.json', 'wb')
	# json.dump(cleaned, fp, indent = 3)
	return render_template('plot.html', name = cleaned)

def main():
    app.run()

if __name__ == '__main__':
    main()
