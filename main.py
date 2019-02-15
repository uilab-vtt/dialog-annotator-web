import os 
import json
import time
import random
from flask import Flask, request, render_template

app = Flask(__name__)
data_path = './data'
response_path = './response'

@app.route('/')
def hello_world():
    return 'color-annotator-web'

@app.route('/survey/<string:books_id>')
def survey_index(books_id):
    return render_template('survey_index.html', books_id=books_id)

@app.route('/survey/<string:books_id>/pretest')
def survey_pretest(books_id):
    return render_template('survey_pretest.html', books_id=books_id)

def get_books(books_id):
    with open('%s/books/%s.json' % (data_path, books_id), 'r') as f:
        books = json.load(f)
    return books

def to_color_hex(value):
    hex_string = hex(int(value)).split('x')[1]
    while len(hex_string) < 2:
        hex_string = '0' + hex_string
    return hex_string

def get_colors():
    colors = []
    for i in range(4):
        for j in range(4):
            for k in range(4):
                r = to_color_hex((255 / 3.0) * i)
                g = to_color_hex((255 / 3.0) * j)
                b = to_color_hex((255 / 3.0) * k)
                colors.append('#%s%s%s' % (r, g, b))
    # colors.sort(key=lambda x: int(x[1:3], 16) + int(x[3:5], 16) + int(x[5:], 16))
    return colors

@app.route('/survey/<string:books_id>/tasks')
def survey_tasks(books_id):
    books = get_books(books_id)
    colors = get_colors()
    return render_template('survey_tasks.html', books_id=books_id, books=books, colors=colors)

def is_response(filename):
    return os.path.exists('%s/%s.json' % (response_path, filename))

def save_response(books_id, response):
    ts = str(int(time.time() * 1000))
    suffix = str(random.randint(0, 1000000))
    filename = '%s_%s_%s' % (books_id, ts, suffix)
    while is_response(filename):
        filename += '_e'
    with open('%s/%s.json' % (response_path, filename), 'w') as f:
        json.dump(response, f)
    return filename

@app.route('/survey/<string:books_id>/submit', methods=['POST'])
def survey_submit(books_id):
    data = json.loads(request.data)
    response = data['responses']
    code = save_response(books_id, response)
    return 'done:%s' % code

@app.route('/survey/<string:books_id>/done/<string:code>')
def survey_done(books_id, code):
    return render_template('survey_done.html', books_id=books_id, code=code)

if __name__ == '__main__':
    app.run(debug=True)