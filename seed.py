"""Utility file to seed poketwitcher database from Pokemon API and Faker data in seed_data/"""

from sqlalchemy import func
from model import User, Pokemon, Sighting
from faker import Faker
from random import choice
import json

from model import connect_to_db, db
from server import app
from datetime import datetime

def json_reader(file_path):
    """Helper function for turning json files into Python dictionaries."""

    with open(file_path) as file:
        json_dict = json.load(file)

    return json_dict

def id_grabber():
    """Helper function to grab all the IDs in the DB for sighting generation."""

    # SELECT pokemon_id FROM pokemon;

    pokemon_ids = []

    all_pogo_json = "/home/vagrant/src/projects/app/static/seed_data/all-pogo.json"

    poke_dict = json_reader(all_pogo_json)

    for key in poke_dict:
        pokemon_ids.append(poke_dict[key].get('id'))

    return pokemon_ids

POKEMON_IDS = id_grabber()

################################################################################

def load_users():
    """Create user with Fake and load into database."""

    print("Users")

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Create new users with Faker
    for i, person in enumerate(range(0, 30)):
        faker = Faker()
        email = faker.email()
        password = faker.password(length=choice(range(10, 16)), special_chars=False, digits=True, upper_case=True, lower_case=True)

        user = User(email=email,
                    password=password)

        # Add to session
        db.session.add(user)

        # Progess yay!
        if i % 10 == 0:
            print(i)

    # Commit all new users to the table
    db.session.commit()

def load_pokemon():
    """Load all the Pokemon Go pokemon (586) from JSON."""

    print("Pokemon")

    Pokemon.query.delete()

    all_pogo_json = "/home/vagrant/src/projects/app/static/seed_data/all-pogo.json"

    # with open(all_pogo_json) as file:
    #     poke_dict = json.load(file)
    poke_dict = json_reader(all_pogo_json)

    for i, key in enumerate(poke_dict):
        pokemon_id = poke_dict[key].get('id')
        name = poke_dict[key].get('name')

        new_pokemon = Pokemon(pokemon_id=pokemon_id, 
                              name=name)

        # Add to session
        db.session.add(new_pokemon)

        # Progess yay!
        if i % 10 == 0:
            print(i)

    # Commit all new pokemon to the table
    db.session.commit()

def load_sightings():
    """Load ratings from u.sightings into database."""

    print("Sightings")

    Sighting.query.delete()

    for i, row in enumerate(range(50)):
        faker = Faker()
        user_id = choice(range(1, 30))
        pokemon_id = choice(POKEMON_IDS)
        timestamp = faker.date_time()

        sighting = Sighting(user_id=user_id,
                            pokemon_id=pokemon_id,
                            timestamp=timestamp)

        # Add to session
        db.session.add(sighting)

        # Progess yay!
        if i % 10 == 0:
            print(i)

    # Commit all new sightings to the table
    db.session.commit()

def set_val_user_id():
    """Set value for the next user_id after seeding database."""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()

def set_val_sighting_id():
    """Set value for the next sighting_id after seeding database."""

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
    set_val_sighting_id()
