from flask import jsonify

from src.common.exceptions import ApplicationError
from src.helpers import apology


def handle_error(e: Exception) -> tuple[str, int]:
    def to_response(message: str, code: int) -> tuple[str, int]:
        return apology(message, code)

    if isinstance(e, ApplicationError):
        return to_response(e.message, e.code)

    return to_response(str(e), 500)
