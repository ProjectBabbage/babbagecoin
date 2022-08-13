from common.models import MINING_REWARD_ADDRESS, PubKey, SignedTransaction

balances = {}


def touch_balance(account: PubKey):
    if account.hash() not in balances:
        balances[account] = 0


def get_balance(account: PubKey):
    touch_balance(account)
    return balances[account.hash()]


def valid_balance(account: PubKey):
    account.dumps() == MINING_REWARD_ADDRESS or balances[account.hash()] >= 0


def update_balances_from_transaction(stx: SignedTransaction, new: bool):
    tx = stx.transaction
    touch_balance(tx.sender)
    if not new:
        tx.amount = -tx.amount
    balances[tx.sender.hash()] -= tx.amount
    touch_balance(tx.receiver)
    balances[tx.receiver.hash()] += tx.amount
    return valid_balance(tx.sender) and valid_balance(tx.receiver)


def update_balances_from_new_transaction(stx):
    update_balances_from_transaction(stx, True)


def update_balances_from_old_transaction(stx):
    update_balances_from_transaction(stx, False)
