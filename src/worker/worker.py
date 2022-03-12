from typing import Optional

import requests

from src.common.hash_service import hash_block
from src.common.models import Block
from src.common.schemas import BlockSchema

url = 'http://127.0.0.1:5000/'
hash_count_before_update = 10000
difficulty = 20000
bound = 2 ** 256 / difficulty


class BlockStore:
    current_block: Optional[Block] = None
    current_block_hash: Optional[str] = None

    def update_block(self):
        print("Updating block...")
        block = get_next_block()
        block.nounce = 0
        block_hash = hash_block(block)

        if self.current_block_hash != block_hash:
            print("Changing block")
            self.current_block = block
            self.current_block_hash = block_hash
        else:
            print("Keeping same block")


def get_next_block() -> Block:
    res = requests.get(f'{url}blocks/current')
    block_schema = BlockSchema()
    print(res.json())
    return block_schema.load(res.json())


def post_mined_block(block: Block):
    block_schema = BlockSchema()

    json_block = block_schema.dumps(block)

    print(json_block)
    res = requests.post(
        f'{url}blocks/minedblock',
        json_block,
        headers={'Content-Type': 'application/json'}
    )


def run():
    block_store = BlockStore()
    block_store.update_block()

    i = 0
    while i < hash_count_before_update:
        block_hash = hash_block(block_store.current_block)
        if int(block_hash, 16) <= bound:
            print("Block mined successfully")
            post_mined_block(block_store.current_block)
            break
            # block_store.update_block()
            i = 0
        else:
            block_store.current_block.nounce += 1
            i += 1
        if i == hash_count_before_update:
            block_store.update_block()
            i = 0

    print("======= WORKER TERMINATED EARLY ========")
