from common.models import Block


difficulty = 2000000
bound = 2**256 // difficulty


def verify_block_hash(block: Block):
    return int(block.hash(recompute=True), 16) <= bound
