from src.common.exceptions import BadRequest


class BalanceTooLow(BadRequest):
    def __init__(self, message="Not enough money"):
        BadRequest.__init__(self, message)


class NotEnoughShares(BadRequest):
    def __init__(self):
        BadRequest.__init__(self, "You don't have enough shares")


class SharesNotFound(BadRequest):
    def __init__(self, symbol: str):
        BadRequest.__init__(self, f"You don't own any shares of {symbol}")
