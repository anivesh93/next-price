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

def main():
    app.run()

if __name__ == '__main__':
    main()
