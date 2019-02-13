import json
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'

def get_books():
    with open('./data/book_data.json', 'r') as f:
        books = json.load(f)
    return books

@app.route('/survey/<string:user_id>')
def survey(user_id):
    books = get_books()
    return render_template('survey.html', user_id=user_id, books=books)

if __name__ == '__main__':
    app.run(debug=True)