class RewardTransactionNotUnique(Exception):
    pass


class InvalidBlockHash(Exception):
    """The block hash does not respect the difficulty constraint"""

    pass


class MissingRewardTransaction(Exception):
    pass


class InvalidBlockHeight(Exception):
    pass


class InvalidSignatureForTransaction(Exception):
    pass


class BadRewardTransaction(Exception):
    pass
