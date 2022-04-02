from common.models import Block


difficulty = 2000000
bound = 2**256 // difficulty


def is_block_hash_valid(block: Block):
    return int(block.hash(recompute=True), 16) <= bound
