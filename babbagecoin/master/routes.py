import requests
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration


from flask import Flask, request

from babbagecoin.common.schemas import (
    PubKeySchema,
    PrivateKeySchema,
    BlockSchema,
    SignedTransactionSchema,
)
from babbagecoin.common.wallet import Wallet
from babbagecoin.master.blockchain_service import (
    get_head,
    block_tbl,
    build_working_block,
    make_primary_between,
    update_blockchain,
)
from babbagecoin.common.context import NetworkContext
from babbagecoin.common.balance import get_balance_of_address
from babbagecoin.master.broadcast_service import broadcast_block, broadcast_transaction
from babbagecoin.master.transaction_service import (
    update_block_transactions,
    update_reward_transaction,
    mem_pool,
)
from babbagecoin.client.client import Client


sentry_sdk.init(dsn=NetworkContext().sentry_dsn, integrations=[FlaskIntegration()])

app = Flask(__name__, static_folder="../webclient/")


@app.get("/")
def print_chain():
    s = ""
    b = get_head()
    while b.height != 0:
        s += b.html()
        b = block_tbl[b.prev_hash]
    return s


@app.get("/greetings")
def hello():
    return {"message": "greetings"}


@app.get("/webclient")
def get_client_html():
    return app.send_static_file("index.html")


@app.get("/webclient/wallet/new")
def create_new_wallet():
    new_wallet = Wallet(load_from_file=False, save_to_file=False)
    return {
        "private_key": PrivateKeySchema.dumps(new_wallet.private_key),
        "public_key": PubKeySchema.dumps(new_wallet.public_key()),
        "address": new_wallet.public_key().hash(),
    }


@app.post("/webclient/wallet/import")
def import_wallet():
    private_key = PrivateKeySchema.load(request.json["private_key"])
    public_key = private_key.derive_public_key()
    address = public_key.hash()
    return {"public_key": PubKeySchema.dumps(public_key), "address": address}


@app.post("/webclient/faucet/request")
def request_faucet():
    amount = request.json["amount"]
    address = request.json["address"]
    print(request.json)
    client = Client()
    if get_balance_of_address(address) < 1000:
        client.send_transaction(receiver=address, amount=amount, fees=0.1)
        return {"amount_requested": amount, "to_address": address}
    else:
        return {"message": "You have a sufficient amount of BBC on your account :)"}


@app.post("/webclient/tx")
def tx():
    amount = request.json["amount"]
    address = request.json["address"]
    private_key = PrivateKeySchema.load(request.json["private_key"])
    client = Client(private_key)
    client.send_transaction(receiver=address, amount=amount, fees=0)
    return {"message": f"You sent {amount} BBC to {address}"}


@app.get("/blocks/working_block")
def get_working_block():
    next_block = build_working_block()
    update_block_transactions(next_block)
    json_block = BlockSchema.dumps(next_block)
    return json_block


@app.get("/blocks/<block_hash>")
def get_block_with_hash(block_hash: str):
    json_block = BlockSchema.dumps(block_tbl[block_hash])
    return json_block


@app.get("/blocks/hashdict")
def send_block_tbl():
    return block_tbl


@app.post("/blocks/minedblock")
def receive_mined_block_from_miner():
    mined_block = BlockSchema.load(request.json)
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
            make_primary_between(prev_b, b)
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
    balance = get_balance_of_address(address)
    return {"balance": balance, "address": address}
