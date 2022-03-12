import requests
from flask import Flask, request

from src.common.hash_service import hash_block
from src.common.hash_service import hash_dict
from src.common.models import Block
from src.common.schemas import BlockSchema
from src.common.wallet import Wallet
from src.master.broadcast_service import broadcast_block

genesis: Block = Block(height=0)
current: Block = genesis
wallet = Wallet()

app = Flask(__name__)


def update_blockchain(block: Block, leaf: Block):
    global current
    if block.prev_hash in hash_dict:
        prev_block = hash_dict[block.prev_hash]
        prev_block.next_blocks.append(block)
        update_hash_dict_all(block)
        if leaf.height > current.height:
            current = leaf


def update_hash_dict_all(block):
    hash_dict[hash_block(block)] = block
    for b in block.next_blocks:
        update_hash_dict_all(b)


def run():
    app.run(debug=True, host="0.0.0.0")


@app.get("/blocks/current")
def send_current_block_to_miner():
    block_schema = BlockSchema()
    json_block = block_schema.dumps(current)
    return json_block


@app.get("/blocks/<block_hash>")
def send_block_with_hash(block_hash: str):
    block_schema = BlockSchema()
    json_block = block_schema.dumps(hash_dict[block_hash])
    return json_block


@app.post("/blocks/minedblock")
def receive_mined_block_from_miner():
    global current
    block_schema = BlockSchema()
    block = block_schema.load(request.json)
    update_blockchain(block, block)  # synchrone et long
    new_block = Block(height=block.height + 1, prev_hash=hash_block(block))
    current.next_blocks.append(new_block)
    current = new_block
    broadcast_block(block)
    return "ok"


@app.post("/blocks/updateblock")
def receive_block_from_network():
    block_schema = BlockSchema()
    leaf = block_schema.load(request.json["block"])

    url = request.json["url"]
    block = leaf

    if hash_block(leaf) not in hash_dict:
        while block.prev_hash not in hash_dict:
            resp = requests.get(
                f"{url}/blocks/{block.prev_hash}",
                headers={"Content-Type": "application/json"},
            )
            prev_block = block_schema.load(resp.json())
            prev_block.next_blocks.append(block)
            block = prev_block
        update_blockchain(block, leaf)
    return "ok"
