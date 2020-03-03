"""Utility file to seed poketwitcher database from Pokemon API and Faker data in seed_data/"""

from sqlalchemy import func
from model import User, Pokemon, Sighting

from model import connect_to_db, db
from server import app
from datetime import datetime


""" TODOs:
* this all needs to be tested
* pokemon seed function incomplete, how do I seed from an API?
* pick an API so I can seed
* need to check on the sequencing table set up and whether or not I need the id in Users and Sightings since those are SERIAL
* Pokemon do not have a SERIAL id so no worries there
* verify namespacing, naming across model/seed/server
* do not currently know how Faker will output my data so strip/split lines are nominal at present
* really check up on 'id', seems like I might not be able to use it
"""


def load_users():
    """Load users from u.user into database."""

    print("Users")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read u.user file and insert data
    for i, row in enumerate(open("seed_data/u.user")):
        row = row.rstrip()
        id, email, password = row.split("|")

        user = User(id=id,
                    email=email,
                    password=password)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

        # progess yay!
        if i % 100 == 0:
            print(i)

    # Once we're done, we should commit our work
    db.session.commit()

def load_pokemon():
    """Load all the Pokemon Go pokemon from API."""

    print("Pokemon")

    Pokemon.query.delete()

    ### insert enumerate function here ###

    db.session.commit()

def load_sightings():
    """Load ratings from u.sightings into database."""

    print("Sightings")

    Sightings.query.delete()

    for i, row in enumerate(open('seed_data/u.sightings')):
        row = row.rstrip()
        sighting_id, user_id, pokemon_id, timestamp = row.split("|")[:4]

        rating = Sighting(sighting_id=sighting_id,
                          user_id=user_id,
                          pokemon_id=pokemon_id,
                          timestamp=timestamp)

        db.session.add(sighting)

        # progess yay!
        if i % 1000 == 0:
            print(i)

    db.session.commit()

def set_val_user_id():
    """Set value for the next user_id after seeding database."""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()

def set_val_sighting_id():
    """Set value for the next user_id after seeding database."""

    # Get the Max sighting_id in the database
    result = db.session.query(func.max(Sighting.sighting_id)).one()
    max_id = int(result[0])

    # Set the value for the next sighting_id to be max_id + 1
    query = "SELECT setval('sightings_sighting_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    load_pokemon()
    load_sightings()
    set_val_user_id()