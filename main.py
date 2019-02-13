from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/survey/<string:user_id>')
def survey(user_id):
    return user_id

if __name__ == '__main__':
    app.run(debug=True)