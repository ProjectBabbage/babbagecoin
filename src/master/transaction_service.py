from src.common.models import Block


def update_block_signed_transactions(block: Block, mem_pool: set):
    block.signed_transactions.extend(list(mem_pool))


def remove_signed_transactions_from_valid_block(mem_pool: set, block: Block):
    for signed_transaction in block.signed_transactions:
        if signed_transaction in mem_pool:
            mem_pool.remove(signed_transaction)


def add_signed_transactions_from_old_block(mem_pool: set, block: Block):
    for signed_tx in block.signed_transactions:
        mem_pool.add(signed_tx)
