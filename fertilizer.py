"""Helper functions for seed."""

import json

def json_reader(file_path):
    """Converts json files into Python dictionaries."""

    with open(file_path) as file:
        json_dict = json.load(file)

    return json_dict

def id_grabber():
    """Grab all the Pokemon IDs possible for sighting generation."""

    # SELECT pokemon_id FROM pokemon;

    pokemon_ids = []

    all_pogo_json = "static/seed_data/all-pogo.json"
    poke_dict = json_reader(all_pogo_json)

    for key in poke_dict:
        pokemon_ids.append(poke_dict[key].get('id'))

    return pokemon_ids

def gender_grouper():
    """Returns dictionaries of all Pokemon grouped by gender."""

    female = {}
    male = {}
    genderless = {}

    pgender_json = "static/seed_data/pgender.json"
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
    """Determines gender of and individual Pokemon."""
    
    female, male, genderless = gender_grouper()
    gender = ""

    if (poke_id in female) and (poke_id not in male):
        gender = 'F'
    elif (poke_id in male) and (poke_id not in female):
        gender = 'M'
    elif poke_id in male and female:
        gender = "F/M"
    elif poke_id in genderless:
        gender = 'N'

    return gender

def type_normalizer():
    """Returns dictionary of correct type for 'Normal' form Pokemon."""
    
    types = {}

    ptype_json = 'static/seed_data/ptype.json'
    type_list = json_reader(ptype_json)

    for i in range(len(type_list)):
        if (type_list[i].get('form') == 'Normal') or ('form' not in type_list[i]):
            poke_id = type_list[i].get('pokemon_id')
            poke_type = type_list[i].get('type')
        elif ('Normal' not in type_list[i].get('form')) and (type_list[i].get('pokemon_id') not in types):
            poke_id = type_list[i].get('pokemon_id')
            poke_type = type_list[i].get('type')
        types[poke_id] = poke_type

    return types

def poke_typer(poke_id):
    """Determines type(s) of an individual Pokemon."""

    types = type_normalizer()

    return types.get(poke_id)

def possibly_ditto(poke_id):
    """Checks whether a Pokemon has a chance of being Ditto instead, returns Boolean."""

    ditto_json = 'static/seed_data/ditto.json'
    ditto_dict = json_reader(ditto_json)

    chance = False
    poke_id = str(poke_id)

    if poke_id in ditto_dict:
        chance = True

    return chance

# def all_types():
#     """All possible Pokemon types from DB."""

#     types = []
#     all_pmon = type_normalizer()
    
#     for pokemon in all_pmon:
#         p_type = all_pmon.get(pokemon)
#         if p_type not in types:
#             types.append(p_type)

#     return types
