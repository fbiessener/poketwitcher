"""Models and database functions for PokéTwitcher project."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import random

db = SQLAlchemy()

class ModelMixin:
    def save(self):
        db.session.add(self)
        db.session.commit()


class User(ModelMixin, db.Model):
    """User of PokéTwitcher website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def create_passhash(self, password):
        self.password = generate_password_hash(password)

    def login(self, password):
        return check_password_hash(self.password, password)

    def as_dict(self):
        """JSON compatible Bootstrap card for rendering search queries."""

        return {'card': f'<div class="card" style="width: 18rem;"><div class="card-body">Results: <a href="/user/{self.user_id}" class="card-link">{self.username}</a><a href="/user/{self.user_id}" class="card-link"><img src="https://res.cloudinary.com/poketwitcher/image/upload/v1585709529/PokeTwitcher/photo-album.png"></a></div></div>'}

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User id={self.user_id} email={self.email}>"


class Pokemon(ModelMixin, db.Model):
    """A Pokémon available in the app Pokémon Go."""

    __tablename__ = "pokemon"

    pokemon_id = db.Column(db.Integer, autoincrement=False, primary_key=True)
    name = db.Column(db.String, nullable=False)
    gender = db.Column(db.String(3), nullable=False)
    # https://docs.sqlalchemy.org/en/13/core/type_basics.html#sqlalchemy.types.ARRAY
    poke_type = db.Column(db.ARRAY(db.String()), nullable=False)
    ditto_chance = db.Column(db.Boolean(), nullable=False)
    # img stored as unique url path ending for Cloudinary location
    img = db.Column(db.String)

    def chance_of_ditto(self):
        """Gives Pokémon with ditto_chance a 16% chance of recorded as Ditto instead in the sightings table."""

        if self.ditto_chance == True:
            # random() returns random floating point number in range [0.0, 1.0)
            if random.random() < 0.16:
                return True

    def as_dict(self):
        """JSON compatible form for search queries."""

        return {'card': f'<div class="card" style="width: 18rem;"><div class="card-body">Results: <a href="/pokemon/{self.name}" class="card-link">{self.name}</a><a href="/pokemon/{self.name}" class="card-link"><img src="https://res.cloudinary.com/poketwitcher/image/upload/v1585709529/PokeTwitcher/{self.img}"></a></div></div>'}

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Pokemon id={self.pokemon_id} name={self.name}>"


class Sighting(ModelMixin, db.Model):
    """Sighting of an individual Pokémon, belongs to a User and a Pokemon."""

    __tablename__ = "sightings"

    sighting_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.pokemon_id'))
    timestamp = db.Column(db.DateTime(), server_default=db.func.current_timestamp())
    # Possible future maps API implementation
    # location = db.Column(db.String(200))

    # Define relationships to User and Pokémon
    user = db.relationship("User", backref=db.backref("sightings", order_by=sighting_id))
    pokemon = db.relationship("Pokemon", backref=db.backref("sightings", order_by=sighting_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Sighting sighting_id={self.sighting_id} user_id={self.user_id} pokemon_id={self.pokemon_id}>"


################################################################################
# Helper functions

def example_data():
    """Create sample data for testing."""

    # Empty out existing data in-between tests
    User.query.delete()
    Pokemon.query.delete()
    Sighting.query.delete()

    # Add sample users, pokemon, sightings
    userA = User(email='some@email.com', password='password')
    userA.create_passhash(password)
    userB = User(email='test@test.com', password='p4ssword')
    userB.create_passhash(password)
    userC = User(email='another@email.com', password='passw0rd')
    userC.create_passhash(password)
    userD = User(email='blank@gmail.com', password='1234')

    bulbasaur = Pokemon(pokemon_id='1', name='Bulbasaur', gender='F/M')
    chansey = Pokemon(pokemon_id='113', name='Chansey', gender='F')
    hitmonlee = Pokemon(pokemon_id='106', name='Hitmonlee', gender='M')
    magnemite = Pokemon(pokemon_id='81', name='Magnemite', gender='N')

    sighting1 = Sighting(user_id=1, 
                         pokemon_id=1, 
                         timestamp=datetime(2011, 3, 1, 23, 20, 8))
    sighting2 = Sighting(user_id=2, 
                         pokemon_id=113, 
                         timestamp=datetime(2001, 4, 5, 11, 1, 1))
    sighting3 = Sighting(user_id=2, 
                         pokemon_id=81, 
                         timestamp=datetime(1991, 8, 2, 10, 12, 6))
    sighting4 = Sighting(user_id=3, 
                         pokemon_id=81, 
                         timestamp=datetime(2017, 5, 4, 13, 8, 7))
    sighting5 = Sighting(user_id=3, 
                         pokemon_id=106, 
                         timestamp=datetime(1976, 1, 6, 6, 43, 2))
    sighting6 = Sighting(user_id=3, 
                         pokemon_id=1, 
                         timestamp=datetime(1981, 7, 8, 7, 55, 3))

    db.session.add_all([userA, userB, userC, userD, bulbasaur, chansey, hitmonlee, 
                        magnemite, sighting1, sighting2, sighting3, sighting4, 
                        sighting5, sighting6])
    db.session.commit()


def connect_to_db(app, db_url="postgresql:///poketwitcher"):
    """Connect the database to Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///poketwitcher'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    db.create_all()

    print("Connected to DB.")
