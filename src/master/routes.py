import json
import requests
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration


from flask import Flask, request

from common.schemas import BlockSchema, SignedTransactionSchema
from common.wallet import Wallet
from master.blockchain_service import (
    get_head,
    block_tbl,
    build_working_block,
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
    b = get_head()
    while b.height != 0:
        s += b.html()
        b = block_tbl[b.prev_hash]
    return s


@app.get("/blocks/working_block")
def send_working_block_to_miner():
    next_block = build_working_block()
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
    mined_block = BlockSchema.load(request.json)
    remove_signed_transactions_from_valid_block(mem_pool, mined_block)
    update_blockchain(mined_block, mined_block)
    broadcast_block(mined_block)
    update_reward_transaction()
    return "ok"


@app.post("/blocks/updateblock")
def receive_block_from_network():
    leaf = BlockSchema.load(request.json["block"])
    url = request.json["url"]
    b = leaf
    if leaf.hash() not in block_tbl:
        while b.prev_hash not in block_tbl:
            print(f"Fetching block: {b.prev_hash}")
            resp = requests.get(
                f"{url}/blocks/{b.prev_hash}",
                headers={"Content-Type": "application/json"},
            )
            prev_b = BlockSchema.load(resp.json())
            prev_b.next_blocks.append(b)
            b = prev_b
        update_blockchain(b, leaf)
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
