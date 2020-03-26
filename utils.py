def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' in session:
            return func(*args, **kwargs)
        else:
            flash('Professor Willows words rang out. \"There\'s a time and a place for everything. But not now!\"')
            return redirect('/user/load', next=request.url)
    return wrapper


def user_free(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return func(*args, **kwargs)
        else:
            flash('Professor Willows words rang out. \"There\'s a time and a place for everything. But not now!\"')
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
