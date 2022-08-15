from common.models import PubKey, SignedTransaction, SUCCESS, REVERTED

balances = {}


def touch_balance(account: PubKey):
    if account.hash() not in balances:
        balances[account.hash()] = 0


def get_balance(account: PubKey):
    touch_balance(account)
    return balances[account.hash()]


def apply_transaction(stx: SignedTransaction):
    tx = stx.transaction
    touch_balance(tx.sender)
    touch_balance(tx.receiver)
    new_sender_balance = balances[tx.sender.hash()] - tx.amount
    if new_sender_balance >= 0:
        balances[tx.sender.hash()] = new_sender_balance
        balances[tx.receiver.hash()] += tx.amount
        stx.status = SUCCESS
    else:
        stx.status = REVERTED


def cancel_transaction(stx: SignedTransaction):
    tx = stx.transaction
    if stx.status == SUCCESS:
        balances[tx.sender.hash()] += tx.amount
        balances[tx.receiver.hash()] -= tx.amount
    else:
        assert stx.status == REVERTED
