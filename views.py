# its dangerous? click?
from flask import Flask, render_template, redirect, request, session, flash
from functools import wraps
# from datetime import datetime

from model import db, User, Pokemon, Sighting

app = Flask(__name__)

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        else:
            flash('Professor Oaks words rang out. \"There\'s a time and a place for everything. But not now!\"')
            return redirect('/login')
    return wrapper

def user_free(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return func(*args, **kwargs)
        else:
            flash('Professor Oaks words rang out. \"There\'s a time and a place for everything. But not now!\"')
            return redirect('/')
    return wrapper

def oak_evaluator(num_sightings, username):
    """Returns evaluation of Pokedex/Life List based on number of sightings a user has."""
    evaluation = ""
    
    if num_sightings <= 10:
        evaluation = f'You still have lots to do, {username}. Look for Pok\xc3\xa9mon in grassy areas.'
    elif 10 < num_sightings <= 50:
        evaluation = f'Good {username}, you\'re trying hard!'
    elif 50 < num_sightings <= 100:
        evaluation = f'You finally got at least 50 species, {username}!'
    elif 100 < num_sightings < 293:
        evaluation = f'You finally got at least 100 species. I can\'t believe how good you are, {username}!'
    elif 293 <= num_sightings < 440:
        evaluation = f'Outstanding! You\'ve become a real pro at this, {username}!'
    elif 440 <= num_sightings < 586:
        evaluation = f'I have nothing left to say! You\'re the authority now, {username}!'
    elif num_sightings == 586:
        evaluation = f'You\'re Pok\xc3\xa9dex is fully complete! Congratulations, {username}!'
    
    return evaluation
################################################################################

@app.route('/')
def index():
    """Homepage."""

    app.logger.info('Rendering homepage... ')
    print('Rendering homepage... ')

    # different view for logged-in user
    # if session.get('user_id'):
    #     return redirect()

    return render_template('homepage.html')


@app.route('/register')
@user_free
def register_new_user():
    """Register form."""

    app.logger.info('Rendering registration form...')
    print("Rendering registration form... ")

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
    print("Rendering login form... ")

    return render_template('login_form.html')


@app.route('/login', methods=['POST'])
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


@app.route('/logout')
@login_required
def logout():
    """Log out user."""

    del session['user_id']

    app.logger.info("User now logged out")
    print("User logged out")
    
    flash('You are now logged out')
    return redirect('/')


@app.route('/user/<int:user_id>')
def user_detail(user_id):
    """A user's list of sightings."""

    user = User.query.get_or_404(user_id)

    # current error: when user in session, can see other user's life lists
    # route change to /myprofile so that get_404 and can't see other user's files
    
    return render_template("user.html", user=user)

@app.route('/user/myprofile')
@login_required
def user_detail(user_id):
    """A user's list of sightings."""

    user = User.query.get_or_404(user_id)

    # current error: when user in session, can see other user's life lists
    # route change to /myprofile so that get_404 and can't see other user's files
    
    flash('Professor Oak: How is your Pokédex coming? Let\'s see…')
    return render_template("user.html", user=user)

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

    flash('Professor Oak: Wonderful! Your work is impeccable. Keep up the good work!')
    return redirect(f"/user/{user_id}", user=user)
