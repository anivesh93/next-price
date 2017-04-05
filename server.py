from flask import Flask, render_template
app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/realtime')
def realtime():
    return render_template('realtime.html')

@app.route('/historical')
def historical():
    return render_template('historical.html')

@app.route('/<symbol>')
def stock(symbol=None):
    return render_template('stock.html')

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

def main():
    app.run()
    

if __name__ == '__main__':
    main()

