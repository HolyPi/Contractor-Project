from flask import Flask, render_template
from flask_pymongo import PyMongo
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost')
mongo = PyMongo(app)
db = client.videogame
inventory = db.videogames


cart = ShoppingCart.get()
videogames.delete_many({})
videogames.insert_many( [
    {'title': 'Persona 3', 'price': 22.22, } ])
    # {'title': 'Persona 5', 'price': 59.99, 'image': <img src= "P5.jpg" height="42" width="42">},
    # {'title': 'Metal Gear Solid Snake Eater', 'price': 14.99, 'image': <img src= "MTGS.png" height="42" width="42">},
    # {'title': 'Danganronpa trilogy', 'price': 59.99, 'image': <img src= "Danganronpa.jpg" height="42" width="42">},
    # {'title': 'Ace attorney', 'price': 14.99, 'image': <img src= "ACE.jpg" height="42" width="42">},
    # {'title': 'The World Ends With You', 'price': 27.99, 'image': <img src= "TWEWY.jpg" height="42" width="42">},
    # {'title': 'Yakuza 0', 'price': 14.49, 'image': <img src= "Yakuza0.jpg" height="42" width="42">},
    # {'title': 'Fire Emblem Fates Birthright', 'price': 19.99, 'image': <img src= "FEB.jpg" height="42" width="42">} ])

# client = MongoClient('mongodb://localhost:27017/')

@app.route('/')
def videogame_index():
    """Show all playlists."""
    return render_template('index.html', videogame=videogame)

@app.route("/cart/add", methods=['POST'])
def add_to_cart():
    cart = ShoppingCart.add(product=request.form['product'], quantity=int(request.form['quantity']))
    return jsonify(cart)


@app.route("/cart")
def view_cart():
    cart = ShoppingCart.get()
    return render_template("cart.html", cart=cart)

@app.route("/cart/remove/<item_id>", methods=['POST'])
def remove_from_cart(item_id):
    cart = ShoppingCart.remove(item_id)
    return jsonify(cart)

# @app.route("/videogames", methods = ['GET'])
# def show_videogame(title):
#         videogame = db.videogame.find({}
#     return render_template('videogame_title.html', videogame = videogame)
