# its dangerous? click?
from flask import Flask, render_template, redirect, request, session, flash

from model import db, User, Pokemon, Sighting
from utils import *

app = Flask(__name__)

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

    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')

    new_user = User(email=email, 
                    username=username, 
                    password=password)

    # new_user = User(**request.form)
    new_user.create_passhash(password)
    new_user.save()

    flash(f'New account: {username} registered! You\'re now ready to log in')
    return redirect('/user/load')


@app.route('/user/login', methods=['POST'])
# @user_free
def login():
    """Logs in user."""

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

#     # Get login_form variables
#     email = request.form["email"]
#     password = request.form["password"]

#     # is this doing what i think it's doing?
#     user = User.query.filter_by(email=email).first()

#     if not user:
#         flash("No such user with {email}")
#         # app.logger.info("No such user with {email}")
#         print("No such user with {email}")
#         return redirect("/login")

#     if not user.login(password):
#         flash("Incorrect password")
#         # app.logger.info("Incorrect password")
#         print("Incorrect password")
#         return redirect("/login")

    # # Add user_id to session for conditional view of templates
    # session["user_id"] = user.user_id
    
    # flash("Logged in successfully!")
    # app.logger.info("User: {user_id} logged in successfully!")
    # print("User {user_id} logged in successfully!")

    # # return redirect(f"/user/{user.user_id}")
    # return redirect("/user/<user_id>", user=user)


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
    pokedex_eval = ''
    # dict of user_id int keys and string values?
    dex_totals = {}

    # largest sighting_id is the total, how do I find that?
    # which side does this need to be on?
    for user in all_users:
        user_total_sightings = Sighting.query.filter(Sighting.user_id == user.user_id).count()
        pokedex_eval = f'{user_total_sightings}/{total_pokemon}'
        dex_totals[User.user_id] = pokedex_eval

    return render_template('all_users.html', all_users=all_users, dex_totals=dex_totals)


@app.route('/pokemon')
def all_pokemon():
    """A list of all users in PokeTwitcher."""

    all_mon = Pokemon.query.order_by(Pokemon.pokemon_id).all()

    return render_template('all_pokemon.html', all_mon=all_mon)


# @app.route('/pokemon/<int:pokemon_id>')
@app.route('/pokemon/<string:pokemon_name>')
def pokemon_detail(pokemon_name):
    """Detail page for an individual Pokemon."""

    # if user not logged-in, no add sighting button? or pop up on attempt?

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

    # Through manual spamming I tested this, and it does work
    if pokemon.chance_of_ditto():
        pokemon = Pokemon.query.filter_by(name='Ditto').first_or_404()

    pokemon_id = pokemon.pokemon_id

    user_sighting = Sighting.query.filter((Sighting.user_id == user_id) & (Sighting.pokemon_id == pokemon_id)).one_or_none()
    
    if user_sighting is None:
        new_sighting = Sighting(user_id=user_id,
                                pokemon_id=pokemon_id)
        new_sighting.save()

    # current error: method not allowed for redirect to user_detail
    # current error: TypeError: add_sighting() got an unexpected keyword argument 'pokemon_name'

    flash('Professor Willow: Wonderful! Your work is impeccable. Keep up the good work!')
    return redirect(f'/user/{user_id}')
