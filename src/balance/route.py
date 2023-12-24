from flask import Blueprint, flash, redirect, render_template, request, session

from src.db import db
from src.helpers import apology, login_required
from src.balance.balance_service import BalanceService

balance_blueprint = Blueprint("balance", __name__, template_folder="templates")


@balance_blueprint.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit():
    """Deposit funds to account"""

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("deposit.html")

    # User reached route via POST (as by submitting a form via POST)
    user_id = session["user_id"]
    sum = request.form.get("sum")
    password = request.form.get("password")

    # Checking for shares number to be positive
    if not sum:
        return apology("Number of shares must be a positive number")

    if not password:
        return apology("Password cannot be empty")

    BalanceService(db).deposit(user_id, float(sum), password)

    flash(f"Successfully added ${sum} to your balance!")

    return redirect("/")


@balance_blueprint.route("/withdraw", methods=["GET", "POST"])
@login_required
def withdraw():
    """Withdraw funds from account."""

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("withdraw.html")

    # User reached route via POST (as by submitting a form via POST)
    user_id = session["user_id"]
    sum = request.form.get("sum")
    password = request.form.get("password")

    # Checking for shares number to be positive
    if not sum:
        return apology("Number of shares must be a positive number")

    if not password:
        return apology("Password cannot be empty")

    BalanceService(db).withdraw(user_id, float(sum), password)

    flash(f"Successfully withdrew ${sum} from your balance!")

    return redirect("/")
