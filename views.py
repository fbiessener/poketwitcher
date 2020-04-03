"""Routes for server."""

# its dangerous? click?
from flask import Flask, render_template, redirect, request, session, flash, jsonify

from model import db, User, Pokemon, Sighting
from utils import *

app = Flask(__name__)

@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 page."""

    return render_template('404.html'), 404


@app.route('/')
def index():
    """Homepage."""

    app.logger.info('Rendering homepage... ')

    return render_template('homepage.html')


@app.route('/about')
def about():
    """About page."""

    app.logger.info('Rendering about page... ')

    return render_template('about.html')


@app.route('/search.json')
def search():
    """Return a user or Pokemon dictionary for this search query."""

    result = request.args.get('search')
    # capitalize() ensures exact match on pokemon name
    pokemon = Pokemon.query.filter_by(name=result.capitalize()).one_or_none()
    user = User.query.filter_by(username=result).one_or_none()

    if pokemon is not None:
        result = jsonify(pokemon.as_dict())
    elif user is not None:
        result = jsonify(user.as_dict())
    else:
        result = {'card': f'<div class="card" style="width: 18rem;"><div class="card-body"><img src="https://res.cloudinary.com/poketwitcher/image/upload/v1585321664/PokeTwitcher/0.png"><br>\'{result}\' did not return any results, please try another search</div></div>'}

    return result

##################################USER ROUTES###################################

@app.route('/user/load')
@user_free
def get_user():
    """Register/login form."""

    app.logger.info('Rendering registration and login forms...')

    return render_template('load_user.html')


@app.route('/user/register', methods=['POST'])
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
def login():
    """Log in user."""

    # test with first or 404
    user = User.query.filter_by(username=request.form.get('username')).first()

    if user.login(request.form.get('password')):
        app.logger.info(f'User: {user.user_id} logged in successfully!')
        session['user_id'] = user.user_id
    else:
        app.logger.info('Username or password is incorrect')
        flash('Username or password is incorrect, please try again')
        return render_template('load_user.html')

    # flash(f'Welcome back, {user.username}!')
    return redirect('/user/my-profile')


@app.route('/user/my-profile')
@login_required
def view_profile():
    """A logged-in user's list of sightings."""

    user_id = session.get('user_id')
    user = User.query.get_or_404(user_id)

    num_sightings = 0
    type_data = {}
    
    if user.sightings:
        # Rendering DB data into forms usable for willow_eval func and pie chart 
        ptypes, type_counts, evaluation = user_sightings_renderer(user)

        flash('Professor Willow: How is your Pokédex coming? Let\'s see…')
        return render_template('user_detail.html', 
                               user=user, 
                               ptypes=ptypes, 
                               type_counts=type_counts, 
                               evaluation=evaluation)
    else:
        evaluation = willow_evaluator(user.username)

        flash('Professor Willow: How is your Pokédex coming? Let\'s see…')
        return render_template('my_profile.html', 
                               user=user, 
                               evaluation=evaluation)


@app.route('/user/<int:user_id>')
def user_detail(user_id):
    """An individual user's list of sightings."""

    user = User.query.get_or_404(user_id)

    if session.get('user_id') and (user.user_id == session.get('user_id')):
        return redirect('/user/my-profile')
    
    num_sightings = 0
    type_data = {}
    
    if user.sightings:
        # Rendering DB data into forms usable for willow_eval func and pie chart 
        ptypes, type_counts, evaluation = user_sightings_renderer(user)

        return render_template('user_detail.html', 
                               user=user, 
                               ptypes=ptypes, 
                               type_counts=type_counts, 
                               evaluation=evaluation)
    else:
        evaluation = willow_evaluator(user.username)
        return render_template('user_detail.html', 
                               user=user, 
                               evaluation=evaluation)


@app.route('/user/all')
def all_users():
    """A list of all users on PokéTwitcher."""

    all_users = User.query.order_by(User.user_id).all()

    total_pokemon = 586
    user_total_sightings = 0
    dex_totals = {}

    for user in all_users:
        user_total_sightings = Sighting.query.filter_by(user_id=user.user_id).count()
        dex_totals[user.user_id] = f'{user_total_sightings}/{total_pokemon}'

    return render_template('all_users.html', 
                           all_users=all_users, 
                           dex_totals=dex_totals)


@app.route('/logout')
@app.route('/user/logout')
@login_required
def logout():
    """Log out user."""

    del session['user_id']

    app.logger.info("User is now logged out")
    
    flash('Successfully logged out!')
    return redirect('/')

################################POKEMON ROUTES##################################

@app.route('/pokemon/all')
@app.route('/pokemon')
def all_pokemon():
    """A list of all Pokémon in Pokémon Go."""

    all_mon = Pokemon.query.order_by(Pokemon.pokemon_id).all()

    return render_template('all_pokemon.html', all_mon=all_mon)


@app.route('/pokemon/<string:pokemon_name>')
def pokemon_detail(pokemon_name):
    """Detail page for an individual Pokémon."""

    # If no user_id in session, Jinja logic shows a different button redirecting 
    # users to log in/register
    user_id = session.get('user_id')
    pokemon = Pokemon.query.filter_by(name=pokemon_name).first_or_404()
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

    # 16% chance logging a sighting of a Pokémon with ditto_chance = True will
    # instead be logged as a Ditto
    # Through manual spamming I tested this, and it does work!
    if pokemon.chance_of_ditto():
        pokemon = Pokemon.query.filter_by(name='Ditto').first_or_404()

    pokemon_id = pokemon.pokemon_id

    user_sighting = Sighting.query.filter((Sighting.user_id == user_id) & (Sighting.pokemon_id == pokemon_id)).one_or_none()
    
    # Ensuring unique Pokémon only in a user's sightings
    if user_sighting is None:
        new_sighting = Sighting(user_id=user_id,
                                pokemon_id=pokemon_id)
        new_sighting.save()

        flash('Professor Willow: Wonderful! Your work is impeccable. Keep up the good work!')
        return redirect(f'/user/{user_id}')
    else:
        flash('Professor Willow: You\'ve already seen this Pokémon!')
        return redirect(f'/user/{user_id}')
