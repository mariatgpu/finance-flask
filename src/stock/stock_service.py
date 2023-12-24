from typing import Any

from cs50 import SQL

from src.common.exceptions import UserNotFound
from src.stock.exceptions import BalanceTooLow, NotEnoughShares, SharesNotFound


class StockService:
    def __init__(self, db: SQL):
        self.db = db

    def get_portfolio(self, user_id: int):
        print(user_id)
        portfolio = self.db.execute("SELECT * FROM portfolios WHERE user_id = ?", user_id)
        print(portfolio)
        return portfolio

    def buy(self, user_id: int, symbol: str, stock: dict[str, Any], amount: int):
        stock_price = float(stock["price"])
        transaction_value: float = amount * stock_price
        rows = self.db.execute("SELECT cash FROM users WHERE id = ?", user_id)

        if len(rows) != 1:
            raise UserNotFound()

        user_cash = float(rows[0]["cash"])

        # Making sure user has enough cash to buy the shares
        if user_cash < transaction_value + 1:
            raise BalanceTooLow()

        # Perform the aquisition and update database
        update_user_cash = user_cash - transaction_value
        self.db.execute(
            "UPDATE users SET cash = ? WHERE id = ?", update_user_cash, user_id
        )

        # Format balance
        balance = f"${update_user_cash:,.2f} (-${transaction_value:,.2f})"

        # Check if stock with specified symbol already exists
        rows = self.db.execute(
            "SELECT shares FROM portfolios WHERE user_id = ? AND symbol = ?",
            user_id,
            symbol,
        )

        if (len(rows) == 0):
            # Add transaction to portfolio database
            self.db.execute(
                "INSERT INTO portfolios (user_id, name, symbol, shares, paid_price, current_price, date, stock_value) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                user_id,
                stock["name"],
                symbol,
                amount,
                stock_price,
                stock_price,
                self.__current_time(),
                stock_price,
            )
        else:
            # Update transaction in portfolio database
            self.db.execute(
                "UPDATE portfolios SET shares = ? WHERE user_id = ? AND symbol = ?",
                int(rows[0]["shares"]) + 1,
                user_id,
                symbol,
            )

        # Add transaction to history database
        self.db.execute(
            "INSERT INTO history (user_id, name, symbol, shares, action, balance, date) VALUES (?, ?, ?, ?, ?, ?, ?)",
            user_id,
            stock["name"],
            symbol,
            amount,
            "BOUGHT",
            balance,
            self.__current_time(),
        )

    def sell(self, user_id: int, symbol: str, stock: dict[str, Any], amount: int):
        owned_stock = self.db.execute(
            "SELECT shares FROM portfolios WHERE user_id = ? AND symbol = ?",
            user_id,
            symbol,
        )

        # Check if user owns shares of the stock
        if not owned_stock:
            raise SharesNotFound(symbol)

        # Check if user has enough shares to sell
        current_shares = sum([stock["shares"] for stock in owned_stock])
        if current_shares < amount:
            raise NotEnoughShares()

        # Retrieve user's balance
        cash = self.db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        cash = cash[0]["cash"]
        # Deposit value of sold shares
        current_price = float(stock["price"])
        cash += amount * current_price

        # Perform the sale
        for info in owned_stock:
            # Update database if user sells less shares than the total amount he owns
            if info["shares"] > amount:
                self.db.execute(
                    "UPDATE portfolios SET shares = ? WHERE user_id = ? AND symbol = ?",
                    info["shares"] - amount,
                    user_id,
                    symbol,
                )
            # Delete stock from portfolio if all shares were sold
            else:
                self.db.execute(
                    "DELETE FROM portfolios WHERE user_id = ? AND symbol = ?",
                    user_id,
                    symbol,
                )

        # Format balance
        balance = f"${cash:,.2f} (+${(amount * current_price):,.2f})"

        # Update user's cash balance
        self.db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, user_id)

        # Add transaction to history database
        self.db.execute(
            "INSERT INTO history (user_id, name, symbol, shares, action, balance, date) VALUES (?, ?, ?, ?, ?, ?, ?)",
            user_id,
            stock["name"],
            symbol,
            amount,
            "SOLD",
            balance,
            self.__current_time(),
        )

    def __current_time(self) -> str:
        from datetime import datetime

        return datetime.now().strftime("%d-%m-%Y %H:%M:%S")
