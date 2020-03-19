"""Helper functions for seed.py."""

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

def genderizer():
    """Allocates gender for Pokemon."""

    female = {}
    male = {}
    none = {}

    pgender_json = "/home/vagrant/src/projects/app/static/seed_data/pgender.json"

    # {[{a: {}, b, c}, {...}], [], ...}
    # b = pokemon_id
    # c = pokemon_name
    gender_dict = json_reader(pgender_json)

    # i want to unpack the gender lists into dictionaries

    #pseudocode
    # key is gender category
    # value is a list of all pokemon with that gender distribution
    # (list of dictionaries)
    for key, value in gender_dict:
        pokemon_id = value[something].get(pokemon_id)
        name = value[something].get(pokemon_name)
        
        if gender_dict[key] == "Genderless":
            none.add("pokemon_id": pokemon_id)
        elif gender_dict[key] == "0M_1F":
            female.add("pokemon_id": pokemon_id)
        elif gender_dict[key] == "1M_0F":
            male.add("pokemon_id": pokemon_id)
        else:
            female.add("pokemon_id": pokemon_id)
            male.add("pokemon_id": pokemon_id)
    
    return female, male, none
