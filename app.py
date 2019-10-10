from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient()
db = client.get_default_database('GameMania')
videogames = db.videogames
cart = db.cart

videogames.delete_many({})
videogames.insert_many(
    [{'title': 'Persona 3', 'price': 22.22, 'image': "https://images-na.ssl-images-amazon.com/images/I/81yTRFRr23L.AC_SL1500_.jpg"},
    {'title': 'Persona 5', 'price': 59.99, 'image': "https://media.gamestop.com/i/gamestop/10146553/Persona-5"},
    {'title': 'Metal Gear Solid: Snake Eater', 'price': 14.99, 'image': "https://http2.mlstatic.com/metal-gear-solid-3-snake-eater-ps2-patch-leia-desc-D_NQ_NP_778579-MLB31218428427_062019-F.jpg"},
    {'title': 'Danganronpa trilogy', 'price': 59.99, 'image': "https://images-na.ssl-images-amazon.com/images/I/81sLio1GoeL._AC_SX430_.jpg"},
    {'title': 'Ace attorney', 'price': 14.99, 'image': "https://vignette.wikia.nocookie.net/aceattorney/images/d/db/JFA_Box_Art.png/revision/latest?cb=20151028223624"},
    {'title': 'The World Ends With You', 'price': 27.99, 'image': "https://media.gamestop.com/i/gamestop/10157970/The-World-Ends-with-You-Final-Remix"},
    {'title': 'Yakuza 0', 'price': 14.49, 'image': "https://images-na.ssl-images-amazon.com/images/I/810MJ9frzIL._SL1500_.jpg"},
    {'title': 'Fire Emblem Fates Birthright', 'price': 19.99, 'image': "https://media.gamestop.com/i/gamestop/10126804/Fire-Emblem-Fates-Birthright?$pdp$"} ])

# client = MongoClient('mongodb://localhost:27017/')

@app.route('/')
def videogame_index():
    """Show all videogames."""
    return render_template('videogame_index.html', videogame=videogames.find())

@app.route('/videogame/<videogame_id>', methods=['GET'])
def videogame_show(videogame_id):
    "Individual Videogame"
    videogame = videogames.find_one({'_id': ObjectId(videogame_id)})
    return render_template('videogame_show.html', videogame=videogame)



@app.route("/cart/add", methods=['POST'])
def add_to_cart():
    "Adds to the cart"
    cart.add(product=request.form['product'], quantity=int(request.form['quantity']))
    return jsonify(cart)


@app.route("/cart")
def view_cart():
    "Views cart"
    cart.get()
    return render_template("cart.html", cart=cart)

@app.route("/cart/remove/<item_id>", methods=['POST'])
def remove_from_cart(item_id):
    "Removes from cart"
    cart = ShoppingCart.remove(item_id)
    return jsonify(cart)

# @app.route("/videogames", methods = ['GET'])
# def show_videogame(title):
#         videogame = db.videogame.find({}
#     return render_template('videogame_title.html', videogame = videogame)
