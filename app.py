from flask import Flask, render_template

app = Flask(__name__)


videogame = [

            { 'title': 'Fire Emblem Three houses' },
            { 'price': '59.99' }
]


@app.route('/')
def index():
    """Return homepage."""
    return render_template('home.html')

@app.route('/videogame')
def videogame_index():
    "Shows videogames"
    return render_template('videogame_index.html', videogame=videogame)


if __name__ == '__main__':
    app.run(debug=True)
