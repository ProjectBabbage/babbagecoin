import time
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
    working_block: Optional[Block] = None
    initial_hash: Optional[str] = None

    def update_working_block(self):
        new_block = get_working_block()
        new_initial_hash = new_block.hash()

        if self.initial_hash != new_initial_hash:
            print("Updating working block")
            new_block.nonce = random.randint(0, 2**64)
            self.working_block = new_block
            self.initial_hash = new_initial_hash
        else:
            print("Keeping same working block")


def get_working_block() -> Block:
    res = requests.get(f"{url_master}blocks/working_block")
    # print(res.json())
    return BlockSchema.load(res.json())


def post_mined_block(block: Block):
    json_block = BlockSchema.dumps(block)

    try:
        requests.post(
            f"{url_master}blocks/minedblock",
            json_block,
            headers={"Content-Type": "application/json"},
        )
    except Exception as e:
        print(f"Could not send mined block: {e}")


def run():
    time.sleep(0.5)  # waiting for the master to be up
    block_store = BlockStore()
    block_store.update_working_block()

    i = 0
    while i < hash_count_before_update:
        block_hash = block_store.working_block.hash()
        if int(block_hash, 16) <= bound:
            print("BLOCK MINED SUCCESSFULLY")
            post_mined_block(block_store.working_block)
            block_store.update_working_block()
            i = 0
        else:
            block_store.working_block.nonce += 1
            block_store.working_block.reset_hash()
            i += 1
        if i == hash_count_before_update:
            block_store.update_working_block()
            i = 0

    print("======= WORKER TERMINATED EARLY ========")
