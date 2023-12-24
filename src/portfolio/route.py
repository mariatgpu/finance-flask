from flask import Blueprint, render_template, session

from src.db import db
from src.helpers import login_required
from src.portfolio.portfolio_service import PortfolioService

portfolio_blueprint = Blueprint("portfolio", __name__, template_folder="templates")


@portfolio_blueprint.route("/")
@login_required
def index():
    """Show portfolio of stocks."""

    user_id = session["user_id"]

    portfolio, cash_left, total_amount = PortfolioService(db).get_and_update_user_portfolio(int(user_id))

    return render_template(
        "index.html",
        portfolio=portfolio,
        cash_left=cash_left,
        total_amount=total_amount,
    )
