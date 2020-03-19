"""Models and database functions for PokeTwitcher project."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

""" TODO:
* test all of this
* verify syntax of Boolean args
* make decision regarding 'type' column in database and possible addtl relational table for it
* make decision regarding 'gender' and possible addtl relational table for it
* make decision for location column and datatype
"""

class ModelMixin:
    def save(self):
        db.session.add(self)
        db.session.commit()


class User(ModelMixin, db.Model):
    """User of PokeTwitcher website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User id={self.user_id} email={self.email}>"

    def create_passhash(self, password):
        self.password = generate_password_hash(password)

    def login(self, password):
        return check_password_hash(self.password, password)


class Pokemon(ModelMixin, db.Model):
    """A Pokemon available in the app Pokemon Go."""

    __tablename__ = "pokemon"

    pokemon_id = db.Column(db.Integer, autoincrement=False, primary_key=True)
    name = db.Column(db.String, nullable=False)
    #############################################################
    # shiny = db.Column(db.Boolean(), nullable=False)
    gender = db.Column(db.String(3))
    # https://docs.sqlalchemy.org/en/13/core/type_basics.html#sqlalchemy.types.ARRAY
    # poke_type = db.Column(db.ARRAY(String), nullable=False)
    # alolan = db.Column(db.Boolean(), nullable=False)
    # isDitto = db.Column(db.Boolean(), nullable=False)
    # img store as url
    # img = db.Column(db.String)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Pokemon id={self.pokemon_id} name={self.name}>"


class Sighting(ModelMixin, db.Model):
    """Sighting of an individual Pokemon, belongs to a User and a Pokemon."""

    __tablename__ = "sightings"

    sighting_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    # If I set pokemon_id to unique, will it allow only one of each for the whole db?
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.pokemon_id'))
    # How do I timestamp a sighting?
    timestamp = db.Column(db.DateTime(), server_default=db.func.current_timestamp())
    ############################################################
    # How do I convert lat and long into a string for this? ###
    # location = db.Column(db.String(200))

    # Define relationships to user and pokemon
    user = db.relationship("User", backref=db.backref("sightings", order_by=sighting_id))
    pokemon = db.relationship("Pokemon", backref=db.backref("sightings", order_by=sighting_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Sighting sighting_id={self.sighting_id} user_id={self.user_id} pokemon_id={self.pokemon_id}>"


################################################################################
# Helper functions

def example_data():
    """Create sample data."""

    # Empty out existing data in-between tests
    User.query.delete()
    Pokemon.query.delete()
    Sighting.query.delete()

    # Add sample data

    # Check the demo for testing Flask on set up


def connect_to_db(app, db_url="postgresql:///poketwitcher"):
    """Connect the database to Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///poketwitcher'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    db.create_all()

    print("Connected to DB.")
