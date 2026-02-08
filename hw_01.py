from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return '<h1>Hello, Flask!</h1>'


@app.route('/username/<username>')
def user(username):
    return f'<h1>Hello, username: {username}!</h1>'


@app.route('/user/<raw_data>', methods=['POST'])
def create_user(raw_data):
    data = {
        'data': raw_data,
    }

    return f'<h1>Hello, create_user {data}!</h1>'


@app.route('/user/<raw_data>', methods=['GET'])
def return_user(raw_data):
    data = {
        'data': raw_data,
    }

    return f'<h1>Hello, return_user {data}!</h1>'


@app.route('/<false_path>')
def f_path(false_path):
    return f'<h1>Not found, {false_path}!</h1>'



if __name__ == '__main__':
    app.run(debug=True)
