"""Utility file to seed poketwitcher database from Pokemon API and Faker data in seed_data/"""

from sqlalchemy import func
from faker import Faker
from random import choice

from model import connect_to_db, db, User, Pokemon, Sighting
from server import app
from fertilizer import *

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
        username = faker.user_name()
        password = faker.password(length=choice(range(10, 16)), special_chars=False, digits=True, upper_case=True, lower_case=True)

        user = User(email=email,
                    username=username,
                    password=password)

        # significantly slows down the db, does work. hash is v long
        user.create_passhash(password)

        # Add to session and commit
        user.save()

        # Progess yay!
        if i % 10 == 0:
            print(i)

def load_pokemon():
    """Load all the Pokemon Go pokemon (586) from JSON."""

    print("Pokemon")

    Pokemon.query.delete()

    all_pogo_json = '/home/vagrant/src/projects/app/static/seed_data/all-pogo.json'
    poke_dict = json_reader(all_pogo_json)

    for i, key in enumerate(poke_dict):
        pokemon_id = poke_dict[key].get('id')
        name = poke_dict[key].get('name')
        gender = genderizer(pokemon_id)
        poke_type = poke_typer(pokemon_id)
        ditto_chance = possibly_ditto(pokemon_id)
        # store as 0.png?
        img = 'https://res.cloudinary.com/poketwitcher/image/upload/v1585321664/PokeTwitcher/0.png.png'

        pokemon = Pokemon(pokemon_id=pokemon_id, 
                          name=name,
                          gender=gender,
                          poke_type=poke_type,
                          ditto_chance=ditto_chance,
                          img=img)
        
        # Add to session and commit
        pokemon.save()

        # Progess yay!
        if i % 10 == 0:
            print(i)

def load_sightings():
    """Load ratings from u.sightings into database."""

    print("Sightings")

    Sighting.query.delete()

    pokemon_ids = id_grabber()

    for i, row in enumerate(range(50)):
        faker = Faker()
        user_id = choice(range(1, 30))
        pokemon_id = choice(pokemon_ids)
        timestamp = faker.date_time()

        sighting = Sighting(user_id=user_id,
                            pokemon_id=pokemon_id,
                            timestamp=timestamp)

        # Add to session and commit
        sighting.save()

        # Progess yay!
        if i % 10 == 0:
            print(i)

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
