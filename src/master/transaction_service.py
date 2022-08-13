import uuid

from common.models import (
    MINING_REWARD_AMOUNT,
    MINING_REWARD_ADDRESS,
    PubKey,
    Block,
    SignedTransaction,
    Transaction,
)
from common.wallet import Wallet

reward_transaction = None
mem_pool = set()
validated_transactions = set()
reward_transaction: Transaction = None
balances = {}


def update_block_transactions(block: Block):
    global mem_pool
    block.signed_transactions.extend(list(mem_pool))


def check_balance(account: PubKey):
    account.dumps() == MINING_REWARD_ADDRESS or balances[account] >= 0


def touch_balance(account: PubKey):
    if account not in balances:
        balances[account] = 0


def update_balances_from_transaction(stx: SignedTransaction):
    tx = stx.transaction
    touch_balance(tx.sender)
    balances[tx.sender] -= tx.amount
    touch_balance(tx.receiver)
    balances[tx.receiver] += tx.amount
    return check_balance(tx.sender) and check_balance(tx.receiver)


def refresh_transactions_from_new_block(block: Block):
    global mem_pool
    global validated_transactions
    excess_transactions = set()
    for stx in block.signed_transactions:
        if stx in validated_transactions:
            excess_transactions.add(stx)
        else:
            validated_transactions.add(stx)
        if stx in mem_pool:
            mem_pool.remove(stx)
        insufficient_funds = update_balances_from_transaction(stx)
    return excess_transactions, insufficient_funds


def refresh_transactions_from_old_block(block: Block):
    global mem_pool
    global validated_transactions
    for stx in block.signed_transactions:
        validated_transactions.remove(stx)
        if stx.transaction.sender.dumps() != MINING_REWARD_ADDRESS:
            mem_pool.add(stx)


def forge_reward_transaction() -> SignedTransaction:
    wallet = Wallet(load_from_file=True)
    transaction = Transaction(
        uuid=str(uuid.uuid4()),
        sender=PubKey(MINING_REWARD_ADDRESS),
        receiver=wallet.get_public_key(),
        amount=MINING_REWARD_AMOUNT,
    )
    return SignedTransaction(
        transaction=transaction,
        signature=wallet.sign(transaction),
    )


reward_transaction = forge_reward_transaction()


def update_reward_transaction():
    global reward_transaction
    reward_transaction = forge_reward_transaction()


def get_reward_transaction():
    return reward_transaction
