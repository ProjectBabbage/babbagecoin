import time
import requests

from src.common.models import Block
from src.common.schemas import BlockSchema

url = 'http://127.0.0.1/'


def get_next_block() -> Block:
    res = requests.get(f'{url}blocks/current')
    block_schema = BlockSchema()
    return block_schema.load(res.json())


def run():
    block = Block("")
    block_schema = BlockSchema()
    json_block = block_schema.dumps(block)

    # b = Block("")
    # difficulty = 2000
    # bound = 2 ** 256 / difficulty
    # print(bound)
    #
    # t = time.time()
    # count = 0
    # while True:
    #     # print(f"{b.nounce}")
    #     h = int(b.hash(), 16)
    #     # print(h)
    #     if h <= bound:
    #         # print(b)
    #         count += 1
    #         if count >= 100:
    #             t2 = time.time()
    #             print(t2 - t)
    #             t = t2
    #             count = 0
    #     b.nounce += 1
