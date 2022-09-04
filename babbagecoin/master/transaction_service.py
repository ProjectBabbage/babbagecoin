import uuid

from babbagecoin.common.models import (
    MINING_REWARD_AMOUNT,
    MINING_REWARD_ADDRESS,
    PubKey,
    Block,
    SignedTransaction,
    Transaction,
)
from babbagecoin.common.wallet import wallet
from babbagecoin.common.balance import apply_transaction, cancel_transaction

reward_transaction = None
mem_pool = set()
validated_transactions = set()
reward_transaction: Transaction = None


def update_block_transactions(block: Block):
    global mem_pool
    block.signed_transactions.extend(list(mem_pool))


def refresh_transactions_from_new_block(block: Block):
    global mem_pool
    global validated_transactions
    excess_transactions = set()
    miner = block.signed_transactions[0].transaction.receiver
    for stx in block.signed_transactions:
        if stx in validated_transactions:
            excess_transactions.add(stx)
        else:
            validated_transactions.add(stx)
            apply_transaction(miner, stx)
        if stx in mem_pool:
            mem_pool.remove(stx)
    return excess_transactions


def refresh_transactions_from_old_block(block: Block):
    global mem_pool
    global validated_transactions
    miner = block.signed_transactions[0].transaction.receiver
    for stx in block.signed_transactions:
        if stx in validated_transactions:
            validated_transactions.remove(stx)
        cancel_transaction(miner, stx)
        if stx.transaction.sender.dumps() != MINING_REWARD_ADDRESS:
            mem_pool.add(stx)


def forge_reward_transaction() -> SignedTransaction:
    transaction = Transaction(
        uuid=str(uuid.uuid4()),
        sender=PubKey(MINING_REWARD_ADDRESS),
        receiver=wallet.public_key().hash(),
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


def get_mem_pool():
    return mem_pool


def get_validated_transactions():
    return validated_transactions
