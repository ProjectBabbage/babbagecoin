import json
import requests
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration


from flask import Flask, request

from common.schemas import BlockSchema, SignedTransactionSchema
from common.wallet import Wallet
from master.blockchain_service import (
    get_current,
    block_tbl,
    build_next_block_from_current,
    update_blockchain,
    compute_balance,
)
from common.ips import get_sentry_dsn
from master.broadcast_service import broadcast_block, broadcast_transaction
from master.transaction_service import (
    remove_signed_transactions_from_valid_block,
    mem_pool,
    update_block_signed_transactions,
    update_reward_transaction,
)

wallet = Wallet()

sentry_sdk.init(dsn=get_sentry_dsn(), integrations=[FlaskIntegration()])
app = Flask(__name__)


def run():
    app.run(debug=True, host="0.0.0.0")


@app.get("/")
def print_chain():
    s = ""
    block_iter = get_current()
    while block_iter.height != 0:
        s += block_iter.html()
        block_iter = block_tbl[block_iter.prev_hash]
    return s


@app.get("/blocks/current")
def send_current_block_to_miner():
    next_block = build_next_block_from_current()
    update_block_signed_transactions(next_block, mem_pool)
    json_block = BlockSchema.dumps(next_block)
    return json_block


@app.get("/blocks/<block_hash>")
def send_block_with_hash(block_hash: str):
    json_block = BlockSchema.dumps(block_tbl[block_hash])
    return json_block


@app.get("/blocks/hashdict")
def send_block_tbl():
    return block_tbl


@app.post("/blocks/minedblock")
def receive_mined_block_from_miner():
    block = BlockSchema.load(request.json)
    remove_signed_transactions_from_valid_block(mem_pool, block)
    update_blockchain(block, block)
    broadcast_block(block)
    update_reward_transaction()
    return "ok"


@app.post("/blocks/updateblock")
def receive_block_from_network():
    leaf = BlockSchema.load(request.json["block"])

    url = request.json["url"]
    block = leaf

    if leaf.hash() not in block_tbl:
        while block.prev_hash not in block_tbl:
            print(f"Fetching block: {block.prev_hash}")
            resp = requests.get(
                f"{url}/blocks/{block.prev_hash}",
                headers={"Content-Type": "application/json"},
            )
            prev_block = BlockSchema.load(resp.json())
            prev_block.next_blocks.append(block)
            block = prev_block
        update_blockchain(block, leaf)
    return "ok"


@app.post("/transactions/emit")
def emit_transaction():
    signed_transaction = SignedTransactionSchema.load(request.json)
    mem_pool.add(signed_transaction)
    broadcast_transaction(signed_transaction)
    return "ok"


@app.post("/transactions/add")
def add_transaction():
    signed_transaction = SignedTransactionSchema.load(request.json)
    mem_pool.add(signed_transaction)
    return "ok"


@app.get("/addresses/<address>/balance")
def get_balance(address: str):
    balance = compute_balance(address)
    return json.dumps({"balance": balance, "address": address})
