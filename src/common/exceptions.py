class DuplicatedTransaction(Exception):
    pass


class RewardTransactionNotUnique(Exception):
    pass


class InvalidBlockHash(Exception):
    """The block hash does not respect the difficulty constraint"""

    pass


class InvalidSignatureForTransaction(Exception):
    pass


class BadRewardTransaction(Exception):
    pass
