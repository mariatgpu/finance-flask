from cs50 import SQL
from werkzeug.security import check_password_hash, generate_password_hash

from src.auth.exceptions import (
    IncorrectPassword,
    IncorrectUsername,
    IncorrectUsernameOrPassword,
)
from src.common.exceptions import UserNotFound


class AuthService:
    def __init__(self, db: SQL):
        self.db = db

    def login(self, username: str, password: str) -> int:
        # Query database for username
        rows = self.db.execute("SELECT * FROM users WHERE username = ?", username)

        print(rows)

        if len(rows) != 1:
            raise UserNotFound()

        user = rows[0]
        hash: str = user["hash"]

        print(hash)

        # Ensure username exists and password is correct
        if not check_password_hash(hash, password):
            raise IncorrectUsernameOrPassword()

        print(user["id"])

        return user["id"]

    def register(self, username: str, password: str, confirmation: str):
        if not self.__is_username_valid(username):
            raise IncorrectUsername()

        if not self.__is_password_valid(password):
            raise IncorrectPassword()

        if password != confirmation:
            raise IncorrectPassword("Passwords do not match")

        # Make sure the name isn't registered already or the field is empty
        if len(self.db.execute("SELECT * FROM users WHERE username = ?", username)) > 0:
            raise IncorrectUsername("Username already taken")

        # Query database for username
        self.db.execute(
            "INSERT INTO users (username, hash) VALUES(?, ?);",
            username,
            generate_password_hash(password),
        )

    def __is_username_valid(self, username: str) -> bool:
        import re

        return bool(re.search("^(?=.{4,20}$)(?![_.])[a-zA-Z0-9._]+$", username))

    def __is_password_valid(self, password: str) -> bool:
        import re

        return bool(
            re.search(
                "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$()!%*?&])[A-Za-z\\d@$()!%*?&]{8,}$",
                password,
            )
        )
