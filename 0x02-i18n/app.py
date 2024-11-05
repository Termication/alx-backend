#!/usr/bin/env python3
"""
Flask application with localization and timezone support.
"""
import locale
from flask import (
    Flask,
    render_template,
    request,
    g
)
from flask_babel import Babel
from datetime import timezone as tmzn
from datetime import datetime
from pytz import timezone
import pytz.exceptions
from typing import (
    Dict,
    Union
)


class Config(object):
    """
    Configuration settings for Babel.
    """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)

# User data with locale and timezone preferences
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user() -> Union[Dict, None]:
    """
    Retrieves user data based on the 'login_as' query parameter.
    Returns None if the user ID is not found.
    """
    user_id = request.args.get('login_as')
    if user_id and int(user_id) in users:
        return users.get(int(user_id))
    return None


@app.before_request
def before_request():
    """
    Prepares user data and current time before handling a request.
    """
    user = get_user()
    g.user = user
    
    # Get the current time in the user's timezone
    time_now = pytz.utc.localize(datetime.utcnow())
    time = time_now.astimezone(timezone(get_timezone()))
    
    # Set the locale for time formatting
    locale.setlocale(locale.LC_TIME, (get_locale(), 'UTF-8'))
    
    # Format time and store in the Flask global object
    fmt = "%b %d, %Y %I:%M:%S %p"
    g.time = time.strftime(fmt)


@babel.localeselector
def get_locale():
    """
    Determines the best language match for the user.
    """
    loc = request.args.get('locale')
    if loc in app.config['LANGUAGES']:
        return loc
    if g.user:
        loc = g.user.get('locale')
        if loc in app.config['LANGUAGES']:
            return loc
    loc = request.headers.get('locale')
    if loc in app.config['LANGUAGES']:
        return loc
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@babel.timezoneselector
def get_timezone():
    """
    Determines the appropriate timezone for the user.
    """
    tzone = request.args.get('timezone')
    if tzone:
        try:
            return timezone(tzone).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    if g.user:
        try:
            tzone = g.user.get('timezone')
            return timezone(tzone).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route('/', strict_slashes=False)
def index() -> str:
    """
    Renders the main page.
    """
    return render_template('5-index.html')


if __name__ == "__main__":
    app.run(port="5000", host="0.0.0.0", debug=True)
