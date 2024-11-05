#!/usr/bin/env python3
"""
Flask application with localization and timezone support.
"""
from flask import Flask, render_template, request, g
from flask_babel import Babel
from datetime import timezone as tmzn
from pytz import timezone
import pytz.exceptions
from typing import Dict, Union


class Config(object):
    """
    Configuration for Babel including languages and timezone.
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
    Retrieves user data based on 'login_as' query parameter.
    Returns None if user ID is not found.
    """
    user_id = request.args.get("login_as")
    if user_id and int(user_id) in users:
        return users.get(int(user_id))
    return None


@app.before_request
def before_request():
    """
    Stores user data in Flask's g object for use in requests.
    """
    g.user = get_user()


@babel.localeselector
def get_locale():
    """
    Determines the best language based on query parameters, user settings, or headers.
    """
    locale = request.args.get("locale")
    if locale in app.config["LANGUAGES"]:
        return locale
    if g.user:
        locale = g.user.get("locale")
        if locale in app.config["LANGUAGES"]:
            return locale
    locale = request.headers.get("locale")
    if locale in app.config["LANGUAGES"]:
        return locale
    return request.accept_languages.best_match(app.config["LANGUAGES"])


@babel.timezoneselector
def get_timezone():
    """
    Determines the appropriate timezone from query parameters or user settings.
    """
    timezone_param = request.args.get("timezone")
    if timezone_param:
        try:
            return timezone(timezone_param).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    if g.user:
        try:
            timezone_param = g.user.get("timezone")
            return timezone(timezone_param).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    return app.config["BABEL_DEFAULT_TIMEZONE"]


@app.route("/", strict_slashes=False)
def index() -> str:
    """
    Renders the main page.
    """
    return render_template("5-index.html")


if __name__ == "__main__":
    app.run(port="5000", host="0.0.0.0", debug=True)
