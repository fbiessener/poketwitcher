"""General utilities file for routes in views."""

from flask import Flask, session
from functools import wraps
from model import User, Pokemon, Sighting

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        else:
            flash('Professor Willows words rang out. \"There\'s a time and a place for everything. But not now!\"')
            # url_for(get_user) ? needs to test
            return redirect(url_for('get_user'), next=request.url)
    return wrapper

def user_free(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return func(*args, **kwargs)
        else:
            flash('Professor Willows words rang out. \"There\'s a time and a place for everything. But not now!\"')
            # redirect to page they were on?
            return redirect('/')
    return wrapper

def willow_evaluator(username, num_sightings=0):
    """Returns evaluation of Pokedex/Life List based on number of sightings a user has."""

    evaluation = ""
    
    if num_sightings <= 10:
        evaluation = f'Professor Willow: You still have lots to do, {username}. Look for Pok\u00E9mon in grassy areas.'
    elif 10 < num_sightings <= 50:
        evaluation = f'Professor Willow: Good {username}, you\'re trying hard!'
    elif 50 < num_sightings <= 100:
        evaluation = f'Professor Willow: You finally got at least 50 species, {username}!'
    elif 100 < num_sightings < 293:
        evaluation = f'Professor Willow: You finally got at least 100 species. I can\'t believe how good you are, {username}!'
    elif 293 <= num_sightings < 440:
        evaluation = f'Professor Willow: Outstanding! You\'ve become a real pro at this, {username}!'
    elif 440 <= num_sightings < 586:
        evaluation = f'Professor Willow: I have nothing left to say! You\'re the authority now, {username}!'
    elif num_sightings == 586:
        evaluation = f'Professor Willow: You\'re Pok\u00E9dex is fully complete! Congratulations, {username}!'
    
    return evaluation

def user_sightings_renderer(user):
    num_sightings = 0
    type_data = {}
    
    if user.sightings:
        # Rendering DB data into forms usable for Willow_eval func and pie chart 
        for row in user.sightings:
            num_sightings += 1
            pokemon = Pokemon.query.get(row.pokemon_id)
            # Convert from list to string to avoid Unhashable Type error
            p_type = ' '.join(pokemon.poke_type)
            if p_type in type_data:
                type_data[p_type] += 1
            else:
                type_data[p_type] = 1
        # Unpacking the dictionary into lists for the pie chart to use for labels and data
        ptypes, type_counts = list(type_data.keys()), list(type_data.values())

        evaluation = willow_evaluator(user.username, num_sightings)

        flash('Professor Willow: How is your Pokédex coming? Let\'s see…')
        return render_template('user_detail.html', 
                               user=user, 
                               ptypes=ptypes, 
                               type_counts=type_counts, 
                               evaluation=evaluation)

    # route change to /myprofile so that get_404 and can't see other user's files
    else:
        evaluation = willow_evaluator(user.username)

        flash('Professor Willow: How is your Pokédex coming? Let\'s see…')
        return render_template('my_profile.html', user=user, evaluation=evaluation)
