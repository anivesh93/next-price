from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return 'This is index page.'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

def main():
    app.run()

if __name__ == '__main__':
    main()

