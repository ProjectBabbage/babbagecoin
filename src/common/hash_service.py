import hashlib

from src.common.models import Block
from src.common.schemas import BlockSchema


def hash_block(block: Block) -> str:
    block_schema = BlockSchema()
    json_block = block_schema.dumps(block)
    hasher = hashlib.sha256()
    hasher.update(json_block.encode('utf-8'))
    hasher.digest()
    return hasher.hexdigest()

