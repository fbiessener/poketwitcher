"""Utility file to seed poketwitcher database from Pokemon API and Faker data in seed_data/"""

from sqlalchemy import func
from model import Pokemon # , Sighting, User

from model import connect_to_db, db
from server import app
from datetime import datetime

# ???
import json
import os

from flask import jsonify

json_data = []
json_file = "/home/vagrant/src/projects/app/static/seed_data/test3.json"

file = open(json_file)

json_data = jsonify(file)



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


# # user_id is serialized, I don't think I need it here or in my Fake data
# def load_users():
#     """Load users from u.user into database."""

#     print("Users")

#     # Delete all rows in table, so if we need to run this a second time,
#     # we won't be trying to add duplicate users
#     User.query.delete()

#     # Read u.user file and insert data
#     for i, row in enumerate(open("seed_data/u.user")):
#         row = row.rstrip()
#         user_id, email, password = row.split("|")

#         user = User(user_id=user_id,
#                     email=email,
#                     password=password)

#         # We need to add to the session or it won't ever be stored
#         db.session.add(user)

#         # progess yay!
#         if i % 100 == 0:
#             print(i)

#     # Once we're done, we should commit our work
#     db.session.commit()

# Pokemon ID is specific and needs to be pulled from JSON
# Save API call to JSON file
# def load_json(filename):
#     """Possibly unnessecary helper function."""

#     with open(filename) as file:
#         jsn = json.load(file)
#         file.close()

#         return jsn

def load_pokemon():
    """Load all the Pokemon Go pokemon from JSON."""

    print("Pokemon")

    Pokemon.query.delete()

    # nothing below is working at present
    ############################################################
    # ??? successfully open and print, but can i use
    # response = os.path.join('/home/vagrant/src/projects/app/static/seed_data/test3.json')
    # print(response)

    # with open(response) as test_file:
    #     data = json.loads(test_file.text)
    #     # print(data)

    #     for i, element in test_file:
    #         # print('hello')
    #         pokemon_id, name = test_file[element]

    #         new_pokemon = Pokemon(pokemon_id=pokemon_id, 
    #                               name=name)

    #         db.session.add(new_pokemon)
    #         print(new_pokemon)

    #         # progess yay!
    #         if i % 100 == 0:
    #             print(i)

    # db.session.commit()

# sighting_id is serialized and probably doesn't need to be here either
# def load_sightings():
#     """Load ratings from u.sightings into database."""

#     print("Sightings")

#     Sightings.query.delete()

#     for i, row in enumerate(open('seed_data/u.sightings')):
#         row = row.rstrip()
#         sighting_id, user_id, pokemon_id, timestamp = row.split("|")[:4]

#         rating = Sighting(sighting_id=sighting_id,
#                           user_id=user_id,
#                           pokemon_id=pokemon_id,
#                           timestamp=timestamp)

#         db.session.add(sighting)

#         # progess yay!
#         if i % 1000 == 0:
#             print(i)

#     db.session.commit()

# def set_val_user_id():
#     """Set value for the next user_id after seeding database."""

#     # Get the Max user_id in the database
#     result = db.session.query(func.max(User.id)).one()
#     max_id = int(result[0])

#     # Set the value for the next user_id to be max_id + 1
#     query = "SELECT setval('users_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()

# def set_val_sighting_id():
#     """Set value for the next user_id after seeding database."""

#     # Get the Max sighting_id in the database
#     result = db.session.query(func.max(Sighting.sighting_id)).one()
#     max_id = int(result[0])

#     # Set the value for the next sighting_id to be max_id + 1
#     query = "SELECT setval('sightings_sighting_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    # load_users()
    load_pokemon()
    # load_sightings()
    # set_val_user_id()
    # set_val_sighting_id()
