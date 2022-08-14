from babbagecoin.common.models import Block


difficulty: int = None
bound: int = None


def set_difficulty(new_difficulty: int):
    global difficulty, bound
    difficulty = new_difficulty
    bound = 2**256 // difficulty


set_difficulty(2000000)


def is_block_hash_valid(block: Block):
    return int(block.hash(recompute=True), 16) <= bound
