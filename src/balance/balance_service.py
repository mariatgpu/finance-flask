from cs50 import SQL
from werkzeug.security import check_password_hash

from src.auth.exceptions import IncorrectPassword
from src.balance.exceptions import IncorrectWithdrawSum
from src.common.exceptions import UserNotFound


class BalanceService:
    def __init__(self, db: SQL):
        self.db = db

    def deposit(self, user_id: int, sum: float, password: str):
        rows = self.db.execute("SELECT * FROM users WHERE id = ?", user_id)

        if len(rows) != 1:
            raise UserNotFound()

        user = rows[0]
        hash: str = user["hash"]

        # Ensure password is correct
        if not check_password_hash(hash, password):
            raise IncorrectPassword()

        # Add funds to account
        cash: float = float(user["cash"]) + sum
        self.db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, user_id)

    def withdraw(self, user_id: int, sum: float, password: str):
        rows = self.db.execute("SELECT * FROM users WHERE id = ?", user_id)

        if len(rows) != 1:
            raise UserNotFound()

        user = rows[0]
        hash: str = user["hash"]

        # Ensure password is correct
        if not check_password_hash(hash, password):
            raise IncorrectPassword()

        # Ensure user cannot withdraw more than left cash
        cash = float(user["cash"])
        if sum > cash:
            raise IncorrectWithdrawSum()

        # Withdraw funds from account
        new_cash = cash - sum
        self.db.execute("UPDATE users SET cash = ? WHERE id = ?", new_cash, user_id)
