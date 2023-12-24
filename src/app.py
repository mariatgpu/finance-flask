import src.auth as auth
import src.balance as balance
import src.middlewares as middlewares
import src.portfolio as portfolio
import src.stock as stock
from flask import Flask
from flask_session import Session
from src.helpers import usd


def init():
    app = Flask(__name__)

    auth.init_app(app)
    balance.init_app(app)
    portfolio.init_app(app)
    stock.init_app(app)
    middlewares.init_app(app)

    # Custom filter
    app.jinja_env.filters["usd"] = usd

    # Configure session to use filesystem (instead of signed cookies)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"

    Session(app)

    return app
