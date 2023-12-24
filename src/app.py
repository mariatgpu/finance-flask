from src.helpers import usd
from flask import Flask
import src.auth as auth
import src.balance as balance
import src.portfolio as portfolio
import src.stock as stock
import src.middlewares as middlewares


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

    return app
