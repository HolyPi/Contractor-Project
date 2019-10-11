import os
from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/videogames')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
videogames = db.videogames
comments = db.comments
cart = db.cart
cart.delete_many({})

lass PlaylistsTests(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test the Game homepage."""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Videogame', result.data)

    def test_show_game(self):
        "Test viewing games"
        selection = videogame.find_one
        videogame_id = ObjectId.__str__(selection.get("_id"))
        result = self.client.get(f'/videogame/{videogame_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Persona 3', result.data)

if __name__ == '__main__':
    unittest_main()
