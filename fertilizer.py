"""Helper functions for seed.py."""
import json

""" TODO:
* type needs to be attempted but is less important. only if i want a graphic of poke types as the additional feature
* alolan is a normal read, but I'll have to check my calls for sighting to make sure it's looking for that variable
* isDitto should be a randomized chance when clicking the sighting button
* 
"""

def json_reader(file_path):
    """Converts json files into Python dictionaries."""

    with open(file_path) as file:
        json_dict = json.load(file)

    return json_dict

def id_grabber():
    """Grab all the Pokemon IDs possible for sighting generation."""

    # SELECT pokemon_id FROM pokemon;

    pokemon_ids = []

    all_pogo_json = "/home/vagrant/src/projects/app/static/seed_data/all-pogo.json"
    poke_dict = json_reader(all_pogo_json)

    for key in poke_dict:
        pokemon_ids.append(poke_dict[key].get('id'))

    return pokemon_ids

def gender_grouper():
    """Groups all Pokemon by gender."""

    female = {}
    male = {}
    genderless = {}

    pgender_json = "/home/vagrant/src/projects/app/static/seed_data/pgender.json"
    gender_dict = json_reader(pgender_json)

    # { [ {a: {}, b, c}, ...], ...}
    # b = pokemon_id
    # c = pokemon_name

    # I want to unpack the gender lists into dictionaries for easier look up

    # key is gender category
    # value is a list of all pokemon with that gender distribution
    # (list of dictionaries)
    for key, value in gender_dict.items():
        if key == "Genderless":
            for pokemon in value:
                genderless[pokemon.get("pokemon_id")] = pokemon.get("pokemon_name")
        elif key == "0M_1F":
            for pokemon in value:
                female[pokemon.get("pokemon_id")] = pokemon.get("pokemon_name")
        elif key == "1M_0F":
            for pokemon in value:
                male[pokemon.get("pokemon_id")] = pokemon.get("pokemon_name")
        else:
            for pokemon in value:
                female[pokemon.get("pokemon_id")] = pokemon.get("pokemon_name")
                male[pokemon.get("pokemon_id")] = pokemon.get("pokemon_name")

    return female, male, genderless

def genderizer(poke_id):
    """Determines gender of Pokemon."""
    
    female, male, genderless = gender_grouper()

    gender = ""

    if poke_id in male and female:
        gender = "F/M"
    elif (poke_id in female) and (poke_id not in male):
        gender = 'F'
    elif (poke_id in male) and (poke_id not in female):
        gender = 'M'
    elif poke_id in genderless:
        gender = 'N'

    return gender
