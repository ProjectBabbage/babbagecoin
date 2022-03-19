import random
import requests

from typing import Optional

from common.models import Block
from common.schemas import BlockSchema

url_master = "http://127.0.0.1:5000/"
hash_count_before_update = 1000000
difficulty = 2000000
bound = 2**256 // difficulty


class BlockStore:
    current_block: Optional[Block] = None
    current_block_hash: Optional[str] = None

    def update_block(self):
        print("Updating block...")
        block = get_next_block()
        block.nounce = random.randint(0, 2**100)
        block_hash = block.hash()

        if self.current_block_hash != block_hash:
            print("Changing block")
            self.current_block = block
            self.current_block_hash = block_hash
        else:
            print("Keeping same block")


def get_next_block() -> Block:
    res = requests.get(f"{url_master}blocks/current")
    block_schema = BlockSchema()
    # print(res.json())
    return block_schema.load(res.json())


def post_mined_block(block: Block):
    block_schema = BlockSchema()

    json_block = block_schema.dumps(block)

    print(json_block)
    requests.post(
        f"{url_master}blocks/minedblock",
        json_block,
        headers={"Content-Type": "application/json"},
    )


def run():
    block_store = BlockStore()
    block_store.update_block()

    i = 0
    while i < hash_count_before_update:
        block_hash = block_store.current_block.hash()
        if int(block_hash, 16) <= bound:
            print("BLOCK MINED SUCCESSFULLY")
            post_mined_block(block_store.current_block)
            block_store.update_block()
            i = 0
        else:
            block_store.current_block.nounce += 1
            i += 1
        if i == hash_count_before_update:
            block_store.update_block()
            i = 0

    print("======= WORKER TERMINATED EARLY ========")
