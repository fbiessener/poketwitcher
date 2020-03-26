# its dangerous? click?
from flask import Flask, render_template, redirect, request, session, flash
from functools import wraps
# from datetime import datetime

from model import db, User, Pokemon, Sighting
from fertilizer import all_types

app = Flask(__name__)

# For Pie Charts
TYPES = all_types()

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        else:
            flash('Professor Willows words rang out. \"There\'s a time and a place for everything. But not now!\"')
            return redirect('/login')
    return wrapper

def user_free(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return func(*args, **kwargs)
        else:
            flash('Professor Willows words rang out. \"There\'s a time and a place for everything. But not now!\"')
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

################################################################################

@app.route('/test')
def test():
    """testing my new bootstrap and charts, delete later"""

    user = User.query.get(3)
    evaluation = willow_evaluator(5, user.username)

    # return render_template('pokemon_detail.html', user=user, pokemon='Bulbasaur', users_with=12, users_without=18)
    return render_template('user_detail.html', user=user, evaluation=evaluation)


@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    """Homepage."""

    app.logger.info('Rendering homepage... ')

    # different view for logged-in user
    # if session.get('user_id'):
    #     return redirect()

    return render_template('homepage.html')


@app.route('/register')
@user_free
def register_new_user():
    """Register form."""

    app.logger.info('Rendering registration form...')

    return render_template("register_form.html")


@app.route('/register', methods=["POST"])
# @user_free
def add_new_user():
    """Add a new user to the database."""

    app.logger.info('Adding new user to DB...')   
    user_data = request.form
    app.logger.info(f'User data: {user_data}')

    email = request.form.get("email")
    password = request.form.get("password")

    new_user = User(email=email, password=password)
    new_user.create_passhash(password)

    new_user.save()

    flash(f"New account: {email} registered!")
    return redirect("/login")


@app.route('/login')
@user_free
def login_form():
    """Log-in form."""

    app.logger.info("Rendering login form... ")

    return render_template('login_form.html')


@app.route('/user/login', methods=['POST'])
# @user_free
def login():
    """Logs in user."""

    user = User.query.filter_by(email=request.form.get('email')).first()

    if user.login(request.form.get('password')):
        app.logger.info('Login successful... ')
        session['user_id'] = user.user_id
    else:
        app.logger.info('Login failed!')
        return render_template('login.html')

    return redirect(f'/user/{user.user_id}')

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


@app.route('/user/logout')
@login_required
def logout():
    """Log out user."""

    del session['user_id']

    app.logger.info("User now logged out")
    
    flash('You are now logged out')
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
            p_type = " ".join(pokemon.poke_type)
            if p_type in type_data:
                type_data[p_type] += 1
            else:
                type_data[p_type] = 1
        # Unpacking the dictionary into lists for the pie chart to use for labels and data
        ptypes, type_counts = list(type_data.keys()), list(type_data.values())

        evaluation = willow_evaluator(user.username, num_sightings)

        # current error: breaking when a user doesn't have any sightings

        return render_template("user_detail.html", 
                               user=user, 
                               ptypes=ptypes, 
                               type_counts=type_counts, 
                               evaluation=evaluation)
    else:
        evaluation = willow_evaluator(user.username)
        return render_template("user_detail.html", user=user, evaluation=evaluation)

@app.route('/user/myprofile')
@login_required
def view_profile(user_id):
    """A user's list of sightings."""

    user = User.query.get_or_404(user_id)

    # current error: when user in session, can see other user's life lists
    # route change to /myprofile so that get_404 and can't see other user's files
    
    flash('Professor Willow: How is your Pokédex coming? Let\'s see…')
    return render_template("my_profile.html", user=user)

@app.route('/pokemon')
def all_pokemon():
    """A list of all Pokemon in Pokemon Go."""

    all_mon = Pokemon.query.order_by(Pokemon.pokemon_id).all()

    return render_template("all_pokemon.html", all_mon=all_mon)


@app.route('/pokemon/<string:pokemon_name>')
def pokemon_detail(pokemon_name):
    """Detail page for an individual Pokemon."""

    user_id = session.get('user_id')
    pokemon = Pokemon.query.filter_by(name=pokemon_name).first_or_404()

    # if user not logged-in, no add sighting button? or pop up on attempt?
    # alter type to appear as something other than an array with Jinja

    return render_template("pokemon.html", pokemon=pokemon, user_id=user_id)


@app.route('/pokemon/<string:pokemon_name>', methods=['POST'])
def add_sighting(pokemon):
    """Add new sighting to a user's Life List."""

    new_sighting = Sighting(user_id=user_id,
                            pokemon_id=pokemon_id)
    new_sighting.save()

    # current error: method not allowed for redirect to user_detail

    flash('Professor Willow: Wonderful! Your work is impeccable. Keep up the good work!')
    return redirect(f"/user/{user_id}", user=user)
