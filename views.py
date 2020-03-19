from flask import Flask, render_template, redirect, request, flash

from model import User

app = Flask(__name__)


@app.route('/')
def index():
    """Homepage."""

    app.logger.info("Rendering homepage... ")
    print("Rendering homepage... ")

    return render_template('homepage.html')


@app.route('/register')
def register_new_user():
    """Register form."""

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

    return render_template("pokemon.html", pokemon=pokemon)


@app.route('/pokemon/<string:pokemon_name>', methods=['POST'])
def add_sighting(pokemon):
    """Add new sighting to a user's Life List."""

    new_sighting = Sighting(user_id=user_id,
                            pokemon_id=pokemon_id)
    new_sighting.save()

    return redirect("/user/<user_id>")

