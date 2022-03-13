import requests
from flask import Flask, request

from src.common.hash_service import hash_block
from src.common.schemas import BlockSchema, SignedTransactionSchema
from src.common.wallet import Wallet
from src.master.blockchain_service import hash_dict, build_next_block_from_current, update_blockchain
from src.master.broadcast_service import broadcast_block
from src.master.transaction_service import remove_signed_transactions_from_valid_block, mem_pool
from src.master.transaction_service import update_block_signed_transactions

wallet = Wallet()

app = Flask(__name__)


def run():
    app.run(debug=True, host="0.0.0.0")


@app.get("/blocks/current")
def send_current_block_to_miner():
    next_block = build_next_block_from_current()
    update_block_signed_transactions(next_block, mem_pool)
    block_schema = BlockSchema()
    json_block = block_schema.dumps(next_block)
    return json_block


@app.get("/blocks/<block_hash>")
def send_block_with_hash(block_hash: str):
    block_schema = BlockSchema()
    json_block = block_schema.dumps(hash_dict[block_hash])
    return json_block


@app.get("/blocks/hashdict")
def send_hash_dict():
    return f"{hash_dict}"


@app.post("/blocks/minedblock")
def receive_mined_block_from_miner():
    block_schema = BlockSchema()
    block = block_schema.load(request.json)
    remove_signed_transactions_from_valid_block(mem_pool, block)
    update_blockchain(block, block)  # synchrone et long
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
            print(f"Fetching block: {block.prev_hash}")
            resp = requests.get(
                f"{url}/blocks/{block.prev_hash}",
                headers={"Content-Type": "application/json"},
            )
            prev_block = block_schema.load(resp.json())
            prev_block.next_blocks.append(block)
            block = prev_block
        update_blockchain(block, leaf)
    return "ok"


@app.post("/transactions/add")
def add_transaction():
    signed_transaction_schema = SignedTransactionSchema()
    signed_transaction = signed_transaction_schema.load(request.json)
    mem_pool.add(signed_transaction)
    return "ok"
