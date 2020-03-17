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
* app.logger.info() not printing to server log?
"""

@app.route('/')
def index():
    """Homepage."""

    app.logger.info("Rendering homepage... ")
    print("Rendering homepage... ")

    return render_template("homepage.html")


@app.route('/register')
def register_new_user():
    """Register form."""

    ### needs to flash and redirect to login if email already exists in database ###

    ### update password form eventually? ###

    # app.logger.info("Rendering registration form... ")
    print("Rendering registration form... ")

    return render_template("register_form.html")


@app.route('/register', methods=["POST"])
def add_new_user():
    """Add a new user to the database."""

    email = request.form.get("email")
    password = request.form.get("password")

    account_available = User.query.filter_by(email=email).first()

    if account_available is not None:
        flash(f"Account already registered to {email}, please log in.")
        # app.logger.info(f'{email} already in DB')
        print(f'{email} already in DB')
    else:
        new_user = User(email=email, password=password)
        #hashing password before storing it
        new_user.create_passhash(password)

        new_user.save()

        flash(f"User {email} added")
        # app.logger.info(f'User {email} added')
        print(f"User {email} added")
    return redirect("/login")


@app.route('/login')
def login_form():
    """Log-in form."""

    # app.logger.info("Rendering login form... ")
    print("Rendering login form... ")

    return render_template("login_form.html")


@app.route('/login', methods=["POST"])
def login_user():
    """Logs in user."""

    # Get login_form variables
    email = request.form["email"]
    password = request.form["password"]

    # is this doing what i think it's doing?
    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user with {email}")
        # app.logger.info("No such user with {email}")
        print("No such user with {email}")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        # app.logger.info("Incorrect password")
        print("Incorrect password")
        return redirect("/login")

    # Add user_id to session for conditional view of templates
    session["user_id"] = user.user_id
    
    flash("Logged in successfully!")
    # app.logger.info("User: {user_id} logged in successfully!")
    print("User {user_id} logged in successfully!")

    # return redirect(f"/user/{user.user_id}")
    return redirect("/user/<user_id>", user_id=user_id)


@app.route('/logout')
def logout():
    """Logs out user."""

    del session["user_id"]
    
    flash("You are now logged out")
    # app.logger.info("User now logged out")
    print("User logged out")

    return redirect("/")


@app.route('/user/<int:user_id>')
def user_detail(user_id):
    """A user's sightings list."""

    user = User.query.get_or_404(user_id)
    
    return render_template("user.html", user=user)


@app.route('/pokemon')
def all_pokemon():
    """A list of all Pokemon in Pokemon Go."""

    """
    pseudocode below
    if action = click on pokemon.pokemon_id, following add to session:
        pokemon = Pokemon.query.filter_by(pokemon_id=pokemon_id).first()
        session["pokemon_name"] = pokemon.name 
    """

    all_mon = Pokemon.query.order_by(Pokemon.pokemon_id).all()

    return render_template("all_pokemon.html", all_mon=all_mon)


@app.route('/pokemon/<string:pokemon_name>', methods=["GET"])
def pokemon_detail(pokemon_name):
    """Detail page for an individual Pokemon."""

    # case SENSITIVE when reaching into db
    # string check on poke list page if search
    # if or try 
    pokemon = Pokemon.query.filter_by(name=pokemon_name).first_or_404()

#     if 'user_id' not in session:
#         return render_template("pokemon.html", pokemon=pokemon)
#     else:
#         ### Needs SQL queries for adding a new sighting ###
#         ### Sighting form needs to show the same details as pokemon page as well as letting user log a new sighting ###
#         return render_template("sighting.html", pokemon=pokemon)

    # Bottom of: https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/?highlight=order
    # pokemon = Pokemon.query.get_or_404(pokemon_name)

    return render_template("pokemon.html", pokemon=pokemon)


@app.route('/pokemon/<string:pokemon_name>', methods=['POST'])
def add_sighting(pokemon):
    """Add new sighting to a user's Life List."""

    new_sighting = Sighting(user_id=user_id, 
                            pokemon_id=pokemon.pokemon_id)
    new_sighting.save()

    return redirect("/user/<user_id>")


if __name__ == "__main__":
    app.secret_key = "Gotta catch them all,"
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    from flask_debugtoolbar import DebugToolbarExtension
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
