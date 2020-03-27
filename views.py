# its dangerous? click?
from flask import Flask, render_template, redirect, request, session, flash, jsonify

from model import db, User, Pokemon, Sighting
from utils import *

app = Flask(__name__)

# @app.errorhandler(404)
# def page_not_found(e):
#     # note that we set the 404 status explicitly
#     return render_template('404.html'), 404


@app.route('/test')
def test():
    """Test"""

    user = User.query.get(3)
    # AttributeError: 'InstrumentedList' object has no attribute 'distinct'
    # test = user.sightings.distinct(Pokemon.pokemon_id)
    
    # this finds distinct sightings, how do I use it?
    # test = Sighting.query.filter_by(user_id=user.user_id).distinct()
    # print(test)
    return render_template('test.html')


@app.route('/')
def index():
    """Homepage."""

    app.logger.info('Rendering homepage... ')

    # different view for logged-in user
    # if session.get('user_id'):
    #     return redirect()

    return render_template('homepage.html')


@app.route('/user/load')
@user_free
def get_user():
    """Register/login form."""

    app.logger.info('Rendering registration and login forms...')

    return render_template('load_user.html')


@app.route('/user/register', methods=['POST'])
# @user_free
def add_new_user():
    """Add a new user to the database."""

    app.logger.info('Adding new user to DB...')   
    user_data = request.form
    app.logger.info(f'User data: {user_data}')

    password = request.form.get('password')

    new_user = User(**request.form)
    new_user.create_passhash(password)
    new_user.save()

    flash(f'New account: {new_user.username} registered! You\'re now ready to log in')
    return redirect('/user/load')


@app.route('/user/login', methods=['POST'])
# @user_free
def login():
    """Logs in user."""

    # test with first or 404
    user = User.query.filter_by(username=request.form.get('username')).first()

    if user.login(request.form.get('password')):
        app.logger.info(f'User: {user.user_id} logged in successfully!')
        session['user_id'] = user.user_id
    else:
        app.logger.info('Username or password is incorrect')
        flash('Username or password is incorrect, please try again')
        return render_template('load_user.html')

    flash(f'Welcome back, {user.username}!')
    return redirect('/user/my-profile')


@app.route('/logout')
@app.route('/user/logout')
@login_required
def logout():
    """Logs out user."""

    del session['user_id']

    app.logger.info("User is now logged out")
    
    flash('successfully logged out!')
    return redirect('/')


@app.route('/user/<int:user_id>')
def user_detail(user_id):
    """A user's list of sightings."""

    user = User.query.get_or_404(user_id)

    if session.get('user_id') and (user.user_id == session.get('user_id')):
        return redirect('/user/my-profile')
    
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

        return render_template('user_detail.html', 
                               user=user, 
                               ptypes=ptypes, 
                               type_counts=type_counts, 
                               evaluation=evaluation)
    else:
        evaluation = willow_evaluator(user.username)
        return render_template('user_detail.html', user=user, evaluation=evaluation)


@app.route('/user/my-profile')
@login_required
def view_profile():
    """A logged-in user's list of sightings."""

    user_id = session.get('user_id')
    user = User.query.get_or_404(user_id)

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


@app.route('/user/all')
def all_users():
    """A list of all Pokemon in Pokemon Go."""

    all_users = User.query.order_by(User.user_id).all()

    total_pokemon = 586
    user_total_sightings = 0
    dex_totals = {}

    for user in all_users:
        user_total_sightings = Sighting.query.filter_by(user_id=user.user_id).count()
        dex_totals[user.user_id] = f'{user_total_sightings}/{total_pokemon}'

    return render_template('all_users.html', all_users=all_users, dex_totals=dex_totals)


@app.route('/pokemon')
def all_pokemon():
    """A list of all users of PokeTwitcher."""

    all_mon = Pokemon.query.order_by(Pokemon.pokemon_id).all()

    return render_template('all_pokemon.html', all_mon=all_mon)


@app.route('/pokemon/<string:pokemon_name>')
def pokemon_detail(pokemon_name):
    """Detail page for an individual Pokemon."""

    # if user not logged-in, no add sighting button? or pop up on attempt?

    user_id = session.get('user_id')
    pokemon = Pokemon.query.filter_by(name=pokemon_name).first_or_404()
    # TypeError: object of type 'InstrumentedAttribute' has no len()
    # for kay
    all_sightings = Sighting.query.order_by(Sighting.sighting_id).all()
    p_type = ' '.join(pokemon.poke_type)

    seen = 0
    user_count = User.query.count()

    for row in all_sightings:
        if row.pokemon_id == pokemon.pokemon_id:
            seen +=1
    not_seen = user_count - seen
    totals = [seen, not_seen]

    return render_template('pokemon_detail.html', 
                           pokemon=pokemon, 
                           user_id=user_id, 
                           totals=totals, 
                           p_type=p_type)


@app.route('/pokemon/<string:pokemon_name>', methods=['POST'])
def add_sighting(pokemon_name):
    """Add new sighting to a user's Pokédex."""

    user_id = session.get('user_id')
    user = User.query.get_or_404(user_id)
    
    pokemon = Pokemon.query.filter_by(name=pokemon_name).first_or_404()

    # Through manual spamming I tested this, and it does work
    if pokemon.chance_of_ditto():
        pokemon = Pokemon.query.filter_by(name='Ditto').first_or_404()

    pokemon_id = pokemon.pokemon_id

    user_sighting = Sighting.query.filter((Sighting.user_id == user_id) & (Sighting.pokemon_id == pokemon_id)).one_or_none()
    
    if user_sighting is None:
        new_sighting = Sighting(user_id=user_id,
                                pokemon_id=pokemon_id)
        new_sighting.save()

    flash('Professor Willow: Wonderful! Your work is impeccable. Keep up the good work!')
    return redirect(f'/user/{user_id}')


# @app.route('/search')
# def search_form():
#     """Search."""

#     return


@app.route('/search.json')
def search():
    """Return a user or Pokemon dictionary for this search query."""

    # current error:
    # redirect: http://0.0.0.0:5000/search.json?search=Pikachu
    # output: {
    #            "gender": "F/M", 
    #            "img": "https://res.cloudinary.com/poketwitcher/image/upload/v1585321664/PokeTwitcher/0.png.png", 
    #            "name": "Pikachu", 
    #            "poke_type": [
    #              "Electric"
    #            ], 
    #            "pokemon_id": 25
    #         }

    result = request.args.get('search')
    pokemon = Pokemon.query.filter_by(name=result).one_or_none()
    user = User.query.filter_by(username=result).one_or_none()

    if pokemon is not None:
        result = jsonify(pokemon.as_dict())
    elif user is not None:
        result = jsonify(user.as_dict())
    else:
        result = f'{result} did not return any results, please try again.'

    return result
