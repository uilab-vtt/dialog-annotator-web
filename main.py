import json
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'color-annotator-web'

def get_books():
    with open('./data/book_data.json', 'r') as f:
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

@app.route('/survey/<string:user_id>')
def survey(user_id):
    books = get_books()
    colors = get_colors()
    return render_template('survey.html', user_id=user_id, books=books, colors=colors)

if __name__ == '__main__':
    app.run(debug=True)