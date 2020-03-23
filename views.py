from flask import Flask, render_template, redirect, request, session, flash
from functools import wraps
# from datetime import datetime

from model import db, User, Pokemon, Sighting

app = Flask(__name__)

# Can I factor this out into a helper function?
# def no_dave():
#     if session.get('user_id'):
#         flash('I can\'t let you do that, Dave.')
#         return redirect('/')

def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("I can\'t let you do that, Dave.")
            return redirect(url_for('login_page'))

    return wrapper

@app.route('/')
def index():
    """Homepage."""

    app.logger.info("Rendering homepage... ")
    print("Rendering homepage... ")

    # different view for logged-in user
    # if session.get('user_id'):
    #     return redirect()

    return render_template('homepage.html')


@app.route('/register')
def register_new_user():
    """Register form."""

    # Prevent logged-in users from reaching this page
    if session.get('user_id'):
        flash('I can\'t let you do that, Dave.')
        return redirect('/')

    app.logger.info('Rendering registration form...')
    print("Rendering registration form... ")

    return render_template("register_form.html")


@app.route('/register', methods=["POST"])
def add_new_user():
    """Add a new user to the database."""

    app.logger.info('Adding new user to DB...')   
    user_data = request.form
    app.logger.info(f'User data: {user_data}')

    email = request.form.get("email")
    password = request.form.get("password")

    new_user = User(email=email, password=password)
    new_user.createpass_hash(password)

    new_user.save()

    flash(f"New account: {email} registered!")
    return redirect("/login")


@app.route('/login')
def login_form():
    """Log-in form."""

    # Prevent logged-in users from reaching this page
    if session.get('user_id'):
        flash('I can\'t let you do that, Dave.')
        return redirect('/')

    app.logger.info("Rendering login form... ")
    print("Rendering login form... ")

    return render_template('login_form.html')


@app.route('/login', methods=['POST'])
def login():
    user = User.query.filter_by(email=request.form.get('email')).first()

    if user.login(request.form.get('password')):
        app.logger.info('Login successful... ')
        session['user_id'] = user.user_id
    else:
        app.logger.info('Login failed!')
        return render_template('login.html')

    return redirect('/user/<user_id>', user=user)


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
@login_required
def user_detail(user_id):
    """A user's list of sightings."""

    user = User.query.get_or_404(user_id)

    # user = session.get('user_id')
    
    return render_template("user.html", user=user)


@app.route('/pokemon')
def function():
    """A list of all Pokemon in Pokemon Go."""

    all_mon = Pokemon.query.order_by(Pokemon.pokemon_id).all()

    return render_template("all_pokemon.html", all_mon=all_mon)


@app.route('/pokemon/<string:pokemon_name>')
def pokemon_detail(pokemon_name):
    """Detail page for an individual Pokemon."""

    pokemon = Pokemon.query.filter_by(name=pokemon_name).first_or_404()

    #if user not logged-in, no add sighting? or pop up on attempt?

    return render_template("pokemon.html", pokemon=pokemon)


@app.route('/pokemon/<string:pokemon_name>', methods=['POST'])
def add_sighting(pokemon):
    """Add new sighting to a user's Life List."""

    new_sighting = Sighting(user_id=user_id,
                            pokemon_id=pokemon_id)
    new_sighting.save()

    return redirect("/user/<user_id>")
