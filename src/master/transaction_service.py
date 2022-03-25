import uuid

from common.models import (
    PubKey,
    Block,
    SignedTransaction,
    Transaction,
    MINING_REWARD_ADDRESS,
)
from common.wallet import Wallet

reward_transaction = None
mem_pool = set()
validated_transactions = set()


def update_block_transactions(block: Block):
    global mem_pool
    block.signed_transactions.extend(list(mem_pool))


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
    return excess_transactions


def refresh_transactions_from_old_block(block: Block):
    global mem_pool
    global validated_transactions
    for stx in block.signed_transactions:
        validated_transactions.remove(stx)
        if stx.transaction.sender != MINING_REWARD_ADDRESS:
            mem_pool.add(stx)


def forge_reward_transaction() -> SignedTransaction:
    wallet = Wallet()
    transaction = Transaction(
        uuid=str(uuid.uuid4()),
        sender=PubKey(MINING_REWARD_ADDRESS),
        receiver=wallet.get_public_key(),
        amount=100,
    )
    return wallet.sign(transaction)


reward_transaction = forge_reward_transaction()


def update_reward_transaction():
    global reward_transaction
    reward_transaction = forge_reward_transaction()


def get_reward_transaction():
    return reward_transaction
