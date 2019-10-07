from flask import Flask, render_template
from pymongo import MongoClient

client = MongoClient()
db = client.Playlister
playlists = db.playlists

app = Flask(__name__)

#
# videogame = [
#
#             { 'title': 'Fire Emblem Three houses' },
#             { 'price': '59.99' },
#             { 'title': 'Danganronpa V3'},
#             { 'price': '59.99' }
# ]


@app.route('/')
def videogame_index():
    "Shows videogames"
    return render_template('videogame_index.html', videogame=videogame.find()


if __name__ == '__main__':
    app.run(debug=True)
