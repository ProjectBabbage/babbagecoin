from src.common.models import Block


def update_pool_from_validated_block(mem_pool, block: Block):
    for signed_transaction in block.signed_transactions:
        mem_pool.remove(signed_transaction)
