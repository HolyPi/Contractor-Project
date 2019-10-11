import os
from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/videogames')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
# client = MongoClient()
# db = client.get_default_database('GameMania')
videogames = db.videogames
comments = db.comments
cart = db.cart
cart.delete_many({})


videogames.delete_many({})
# videogames.insert_many(
    # [{'title': 'Persona 3', 'price': 22.22, 'image': "https://images-na.ssl-images-amazon.com/images/I/81yTRFRr23L.AC_SL1500_.jpg"},
    # {'title': 'Persona 5', 'price': 59.99, 'image': "https://media.gamestop.com/i/gamestop/10146553/Persona-5"},
    # {'title': 'Metal Gear Solid: Snake Eater', 'price': 14.99, 'image': "https://http2.mlstatic.com/metal-gear-solid-3-snake-eater-ps2-patch-leia-desc-D_NQ_NP_778579-MLB31218428427_062019-F.jpg"},
    # {'title': 'Danganronpa trilogy', 'price': 59.99, 'image': "https://images-na.ssl-images-amazon.com/images/I/81sLio1GoeL._AC_SX430_.jpg"},
    # {'title': 'Ace attorney', 'price': 14.99, 'image': "https://vignette.wikia.nocookie.net/aceattorney/images/d/db/JFA_Box_Art.png/revision/latest?cb=20151028223624"},
    # {'title': 'The World Ends With You', 'price': 27.99, 'image': "https://media.gamestop.com/i/gamestop/10157970/The-World-Ends-with-You-Final-Remix"},
    # {'title': 'Yakuza 0', 'price': 14.49, 'image': "https://images-na.ssl-images-amazon.com/images/I/810MJ9frzIL._SL1500_.jpg"},
    # {'title': 'Fire Emblem Fates Birthright', 'price': 19.99, 'image': "https://media.gamestop.com/i/gamestop/10126804/Fire-Emblem-Fates-Birthright?$pdp$"} ])

# client = MongoClient('mongodb://localhost:27017/') b

@app.route('/')
def videogame_index():
    """Show all videogames."""
    return render_template('videogame_index.html', videogames=videogames.find())

@app.route('/videogame/<videogame_id>', methods=['GET'])
def videogame_show(videogame_id):
    "Individual Videogame"
    videogame = videogames.find_one({'_id': ObjectId(videogame_id)})
    videogame_comments = comments.find({'_id': ObjectId(videogame_id)})
    return render_template('videogame_show.html', videogame=videogame, comment=videogame_comments)



@app.route("/videogame/<videogame_id>/purchase", methods=['GET'])
def add_to_cart(videogame_id):
    "Adds to the cart"
    game = videogames.find_one({'_id': ObjectId(videogame_id)})
    print(game)
    cartGame = {
        'title': game.get('title'),
        'price': game.get('price'),
        'image': game.get('image')

    }
    cart.insert_one(cartGame)
    return redirect(url_for('videogame_index'))


@app.route("/cart")
def view_cart():
    "Views cart"
    total = 0
    Nothing = ""
    for videogame in cart.find():
        total += int(videogame['price']) * (item['quantity'])
    if cart.count_documents({}) <= 0:
        Nothing = "Nothing inside your cart"
    return render_template("cart.html", videogame=videogame, cart=cart.find(), total = total, Nothing = Nothing)

@app.route("/cart/<videogame_id>/delete", methods=['POST'])
def remove_from_cart(videogame_id):
    "Removes from cart"
    cart.delete_one({'_id':ObjectId('videogame_id')})
    return redirect(url_for('view_cart'))


@app.route('/videogame/comments', methods=['POST'])
def comments_new():
    """Submit a new comment."""
    comment = {
        'title':request.form.get('title'),
        'content':request.form.get('content'),
        'videogame_id': ObjectId(request.form.get('videogame_id'))
    }
    print(comment)
    comment_id = comments.insert_one(comment).inserted_id
    return redirect(url_for('videogame_show', videogame_id=request.form.get('videogame_id')))


@app.route('/videogame/comments/<comment_id>', methods=['POST'])
def comments_delete(comment_id):
    """Action to delete a comment."""
    comment = comments.find_one({'_id': ObjectId(comment_id)})
    comments.delete_one({'_id': ObjectId(comment_id)})
    return redirect(url_for('videogame_show', videogame_id=comment.get('videogame_id')))


@app.route('/videogame/comments/<comment_id>/edit')
def comment_edit(comment_id):
    "Edits comments"
    comment = comments.find_one({'_id': ObjectId(comment_id)})
    return render_template('comment_edit.html', comment=comment)


@app.route('/videogame/comments/<comment_id>', methods=['POST'])
def comment_update(comment_id):
    """Submit an edited comment."""
    updated_comment = {
        'title': request.form.get('title'),
        'content': request.form.get('content'),
        }
    comment.update_one(
        {'_id': ObjectId(comment_id)},
        {'$set': updated_comment})
    return redirect(url_for('videogame_show', comment_id=comment_id))



if app.name == '__main__':
  app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
