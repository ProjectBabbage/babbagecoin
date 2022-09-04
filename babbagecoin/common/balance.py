from babbagecoin.common.models import MINING_REWARD_ADDRESS
from babbagecoin.common.models import SignedTransaction, SUCCESS, REVERTED

balances = {}


def touch_balance(addr: str):
    global balances
    if addr not in balances:
        balances[addr] = 0


def get_balance_of_address(addr: str) -> float:
    touch_balance(addr)
    return balances[addr]


def apply_transaction(miner: str, stx: SignedTransaction):
    global balances
    tx = stx.transaction
    sender = tx.sender.hash()
    receiver = tx.receiver
    touch_balance(sender)
    touch_balance(receiver)
    touch_balance(miner)
    new_sender_balance = balances[sender] - tx.amount - tx.fees
    if new_sender_balance >= 0 or tx.sender.dumps() == MINING_REWARD_ADDRESS:
        balances[sender] = new_sender_balance
        balances[receiver] += tx.amount
        balances[miner] += tx.fees
        tx.status = SUCCESS
    else:
        tx.status = REVERTED


def cancel_transaction(miner: str, stx: SignedTransaction):
    global balances
    tx = stx.transaction
    sender = tx.sender.hash()
    receiver = tx.receiver
    if tx.status == SUCCESS:
        balances[sender] += tx.amount + tx.fees
        balances[receiver] -= tx.amount
        balances[miner] -= tx.fees
    else:
        assert tx.status == REVERTED
