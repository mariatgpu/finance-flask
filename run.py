import os

from src.db import db
from src.app import init
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from src.helpers import apology, login_required, lookup, usd

# Configure session to use filesystem (instead of signed cookies)

app = init()
Session(app)



# @app.route("/")
# @login_required
# def index():
#     """Show portfolio of stocks"""
#     return apology("TODO")


# @app.route("/buy", methods=["GET", "POST"])
# @login_required
# def buy():
#     """Buy shares of stock"""
#     return apology("TODO")


# @app.route("/history")
# @login_required
# def history():
#     """Show history of transactions"""
#     return apology("TODO")


# @app.route("/quote", methods=["GET", "POST"])
# @login_required
# def quote():
#     """Get stock quote."""
#     return apology("TODO")


# @app.route("/sell", methods=["GET", "POST"])
# @login_required
# def sell():
#     """Sell shares of stock"""
#     return apology("TODO")
