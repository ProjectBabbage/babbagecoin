import hashlib
from src.common.models import Block


def hash_block(block: Block) -> str:
    if block.height == 0:
        return ""

    hasher = hashlib.sha256()
    hasher.update(block.prev_hash.encode("utf-8"))
    for transaction in block.signed_transactions:
        hasher.update(transaction.signature.encode("utf-8"))
    hasher.update(f"{block.nounce}".encode("utf-8"))
    return hasher.hexdigest()


hash_dict = {}
