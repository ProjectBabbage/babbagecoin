from flask import Flask, request
from ..common.models import Block
from ..common.schemas import BlockSchema
from ..common.wallet import Wallet

genesis: Block = Block()
current: Block = genesis
wallet = Wallet()

app = Flask(__name__)


def update_current(block: Block):
    global current
    current.next_blocks.append(block)
    current = block


def run():
    app.run(debug=True)


@app.get("/blocks/current")
def send_current_block_to_miner():
    block_schema = BlockSchema()
    json_block = block_schema.dumps(current)
    return json_block


@app.post('/blocks/minedblock')
def receive_mined_block_from_miner():
    block_schema = BlockSchema()
    block = block_schema.load(request.json)
    update_current(block)
    return "ok"


@app.post('/blocks/updateblock')
def receive_block_from_network():
    block_schema = BlockSchema()
    block = block_schema.load(request.json)
    update_current(block)
    return "ok"
