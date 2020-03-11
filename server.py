"""PokeTwitcher."""

from jinja2 import StrictUndefined
# its dangerous? click?
from flask import Flask, render_template, redirect, request, flash, session

from model import connect_to_db, db, User, Pokemon, Sighting

app = Flask(__name__)

app.jinja_env.undefined = StrictUndefined

""" TODO:
* need to test all of this
* need to make sure homepage is different for logged in users
* need to implement log out
* see routes for addtl todos
"""

@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/register', methods=["GET"])
def register_new_user():
    """Register form."""

    ### needs to flash and redirect to login if email already exists in database ###

    ### update password form eventually? ###

    return render_template("register_form.html")

@app.route('/register', methods=["POST"])
def add_new_user():
    """Add a new user to the database."""

    email = request.form.get("email")
    password = request.form.get("password")

    new_user = User(email=email, password=password)

    db.session.add(new_user)
    db.session.commit()

    flash(f"User {email} added")
    return redirect("/")

@app.route('/login', methods=["GET"])
def login_form():
    """Login form."""

    return render_template("login_form.html")


@app.route('/login', methods=["POST"])
def login_user():
    """Logs in user."""

    # Get login_form variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user with {email}")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    # Add user_id to session for conditional view of templates
    session["user_id"] = user.user_id
    
    flash("Logged in successfully!")
    return redirect(f"/{user.user_id}")


# @app.route('/logout')
# def logout():
#     """Logs out user."""

#     del session["user_id"]
    
#     flash("You are now logged out")
#     return redirect("/")


@app.route('/<int:user_id>')
def user_detail(user_id):
    """A user's sightings list."""

    ### make sure html offers links to homepage AND pokemon list AND log new sighting??? ###

#     user = User.query.get(user_id)
    # test user
    user = {'user_id': 1, 'email': 'gurb@blurb.murb'}
    
    return render_template("user.html", user=user)


@app.route('/pokemon')
def all_pokemon():
    """A list of all Pokemon in Pokemon Go."""

    ### Needs to allow logged in users to log a new sighting, get/post separation of route? ###

    """
    pseudocode below
    if action = click on pokemon.pokemon_id, following add to session:
        pokemon = Pokemon.query.filter_by(pokemon_id=pokemon_id).first()
        session["pokemon_name"] = pokemon.name 
    """

    # pokemon = Pokemon.query.order_by(Pokemon.pokemon_id).all()

    # return render_template("all_pokemon.html", pokemon=pokemon)
    return render_template("all_pokemon.html")


# maybe reformat this whole set up and remove sighting.html
# instead do a button that just adds for MVP and a pop-up form with AJAX/JS/JQuery/Bootstrap for beyond
# check syntax on this <pokemon.name>
@app.route('/pokemon/<string:pokemon_name>', methods=["GET"])
def pokemon_detail(pokemon_name):
    """Detail page for an individual Pokemon."""

#     pokemon = Pokemon.query.get(name)

#     if 'user_id' not in session:
#         return render_template("pokemon.html", pokemon=pokemon)
#     else:
#         ### Needs SQL queries for adding a new sighting ###
#         ### Sighting form needs to show the same details as pokemon page as well as letting user log a new sighting ###
#         return render_template("sighting.html", pokemon=pokemon)
    # test pokemon
    pokemon = {'pokemon_id': 1, 'name': 'Bulbasaur'}

    return render_template("pokemon.html", pokemon=pokemon)


if __name__ == "__main__":
    # session instantiation
    app.secret_key = "Gotta catch them all,"

    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    from flask_debugtoolbar import DebugToolbarExtension
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
