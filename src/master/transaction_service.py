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


def update_block_signed_transactions(block: Block, mem_pool: set):
    block.signed_transactions.extend(list(mem_pool))


def remove_signed_transactions_from_valid_block(mem_pool: set, block: Block):
    for signed_transaction in block.signed_transactions:
        if signed_transaction in mem_pool:
            mem_pool.remove(signed_transaction)


def add_signed_transactions_from_old_block(mem_pool: set, block: Block):
    for signed_tx in block.signed_transactions:
        if signed_tx.transaction.sender != MINING_REWARD_ADDRESS:
            mem_pool.add(signed_tx)


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
