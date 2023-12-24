from src.common.exceptions import BadRequest


class IncorrectWithdrawSum(BadRequest):
    def __init__(self, message="Cannot withdraw more than cash left"):
        BadRequest.__init__(self, message)
