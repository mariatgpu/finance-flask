from cs50 import SQL

from src.common.exceptions import InternalServerError
from src.helpers import lookup


class PortfolioService:
    def __init__(self, db: SQL):
        self.db = db

    def get_and_update_user_portfolio(self, user_id: int):
        portfolio = self.db.execute(
            "SELECT * FROM portfolios WHERE user_id = ?", user_id
        )
        cash_left = self.db.execute("SELECT cash FROM users WHERE id = ?", user_id)

        # Getting the amount of cash the user has left to spend
        if cash_left and "cash" in cash_left[0]:
            cash_left = float(cash_left[0]["cash"])
        else:
            cash_left = 0.0

        total_amount = cash_left

        # Updating the current price and the overall stock value for each stock to be displayed in real time
        try:
            for stock in portfolio:
                symbol = stock["symbol"]
                stock_info = lookup(symbol)

                current_price = float(stock_info["price"])
                stock_value = current_price * stock["shares"]

                stock.update(
                    {"current_price": current_price, "stock_value": stock_value}
                )
                total_amount += float(stock["stock_value"])
        except (ValueError, LookupError):
            raise InternalServerError()

        return (portfolio, cash_left, total_amount)
