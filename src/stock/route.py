from flask import Blueprint, flash, redirect, render_template, request, session

from src.db import db
from src.helpers import apology, login_required, lookup, usd
from src.stock.stock_service import StockService

stock_blueprint = Blueprint("stock", __name__, template_folder="templates")


@stock_blueprint.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("buy.html")

    # User reached route via POST (as by submitting a form via POST)
    user_id = session["user_id"]
    symbol = request.form.get("symbol")

    if not symbol:
        return apology("Symbol is not valid")

    stock = lookup(symbol)
    amount = request.form.get("shares")

    # Checking for shares number to be positive
    if not amount or not amount.isdigit():
        return apology("Number of shares must be a positive digit")

    StockService(db).buy(user_id, symbol, stock, int(amount))

    flash(f"Successfully bought {amount} number of {symbol}")

    return redirect("/")


@stock_blueprint.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""

    user_id = int(session["user_id"])

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        print("ADSGFSDGSDGDSGD")
        service = StockService(db)
        return render_template("sell.html", portfolio=service.get_portfolio(user_id))

    # User reached route via POST (as by submitting a form via POST)
    symbol = request.form.get("symbol")

    if not symbol:
        return apology("Symbol is not valid")

    stock = lookup(symbol)
    amount = request.form.get("shares")

    # Checking for shares number to be positive
    if not amount or not amount.isdigit():
        return apology("Number of shares must be a positive digit")

    StockService(db).sell(user_id, symbol, stock, int(amount))

    flash(f"Successfully sold {amount} shares of {symbol}!")

    return redirect("/")


@stock_blueprint.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("quote.html")

    # User reached route via POST (as by submitting a form via POST)
    symbol = request.form.get("symbol")

    if not symbol:
        return apology("Symbol is not valid")

    stock = lookup(symbol)

    # Format price
    stock["price"] = usd(stock["price"])

    return render_template("after_quote.html", stock=stock)


@stock_blueprint.route("/history")
@login_required
def history():
    """Show history of transactions."""

    user_id = session["user_id"]
    history = db.execute("SELECT * FROM history WHERE user_id = ?", user_id)

    return render_template("history.html", history=history)
