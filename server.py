"""PokeTwitcher."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_tob_db, db, User, Pokemon, Sighting

app = Flask(__name__)

app.secret_key = "Gotta catch them all,"

app.jinja_env.undefined = StrictUndefined

""" TODO:
* need to test all of this
* need to modify all_pokemon so a user can also update their sighting list from there as well as the detail page
* need to make sure detail page is linked through all_pokemon page
* need to make sure homepage is different for logged in users
* need to make/implement log out
* need to separate out the get/post register route for brainsafe clarity
* see routes for addtl todos
"""


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('register', methods=["GET", "POST"])
def add_user():
    """Add new user to database."""

    ### this works but I'd rather the route be separated into "get" and "post" so refactor this for simplicity and clarity later also needs to check against db and flash a warning if user is already in db, redirect to login? ###

    ### needs to flash and redirect to login if email already exists in database ###

    ## update password form eventually? ###

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        new_user = User(email=email, password=password)

        db.session.add(new_user)
        db.session.commit()

        flash(f"User {email} added")
    else:
        return render_template("register.html")


@app.route('/login', method=["GET"])
def login_form():
    """Login form."""

    return render_template("login.html")


@app.route('/login', method=["POST"])
def login_user():
    """Logs in user."""

    email = request.form.["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user with {email}")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    # add user_id to session for conditional view of templates
    session["user_id"] = user.user_id
    
    flash("Logged in successfully!")

    return redirect(f"/{user.user_id}")


@app.route('/<int:user_id>')
def user_detail(user_id):
    """User details."""

    ### make sure html offers links to homepage AND pokemon list AND log new sighting??? ###

    user = User.query.get(user_id)

    return render_template("user.html", user=user)

@app.route('/pokemon')
def all_pokemon():
    """A list of all Pokemon in Pokemon Go."""

    ### Needs to allow logged in users to log a new sighting, get/post separation of route? ###

    pokemon = Pokemon.query.order_by(Pokemon.pokemon_id).all()

    return render_template("all_pokemon.html", pokemon=pokemon)


# maybe reformat this whole set up and remove sighting.html
# instead do a button that just adds for MVP and a pop-up form with AJAX/JS/JQuery/Bootstrap for beyond
# check syntax on this <pokemon.name>
@app.route('pokemon/<str:pokemon.name>', methods=["POST"])
def pokemon_detail(pokemon_name):
    """Detail page for an individual Pokemon."""

    pokemon = Pokemon.query.get(name)

    if 'user_id' not in session:
        return render_template("pokemon.html", pokemon=pokemon)
    else:
        ### Needs SQL queries for adding a new sighting ###
        ### Sighting form needs to show the same details as pokemon page as well as letting user log a new sighting ###
        return render_template("sighting.html", pokemon=pokemon)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
