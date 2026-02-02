from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello, Flask!</h1>'


@app.route('/user/<username>')
def user(username):
    return f'<h1>Hello, {username}!</h1>'


@app.route('/<false_path>')
def f_path(false_path):
    return f'<h1>Not found, {false_path}!</h1>'



if __name__ == '__main__':
    app.run(debug=True)
