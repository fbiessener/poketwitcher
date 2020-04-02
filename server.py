"""PokeTwitcher."""

from views import app
from model import connect_to_db

if __name__ == "__main__":
    app.secret_key = "Gotta catch them all,"
    app.debug = False
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

    from jinja2 import StrictUndefined
    app.jinja_env.undefined = StrictUndefined
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    from flask_debugtoolbar import DebugToolbarExtension
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
