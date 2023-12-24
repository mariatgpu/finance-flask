from flask import redirect, render_template, request, session, Blueprint, flash

from src.helpers import apology
from src.db import db
from src.auth.auth_service import AuthService


auth_blueprint = Blueprint("auth", __name__, template_folder="templates")


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via GET (as by clicking a link or via redirect)
    if request.method == "GET":
        return render_template("login.html")

    # User reached route via POST (as by submitting a form via POST)
    username = request.form.get("username")
    password = request.form.get("password")

    # Ensure username was submitted
    if not username:
        return apology("must provide username", 400)

    # Ensure password was submitted
    elif not password:
        return apology("must provide password", 400)

    service = AuthService(db)

    id = service.login(username, password)

    # Remember which user has logged in
    session["user_id"] = id

    # Redirect user to home page
    return redirect("/")


@auth_blueprint.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "GET":
        return render_template("registration.html")

    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    if any(not field for field in [username, password, confirmation]):
        return apology("Fields cannot be empty")

    AuthService(db).register(username, password, confirmation)

    flash("Registered Successful")

    # Redirect user to home page
    return redirect("/login")
