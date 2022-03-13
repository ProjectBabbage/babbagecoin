import json
import os

import requests

from src.common.models import Block, SignedTransaction
from src.common.schemas import BlockSchema, SignedTransactionSchema

known_hosts = [
    os.environ.get("IP_NODE_MARTIAL"),
    os.environ.get("IP_NODE_QUENTIN"),
    os.environ.get("IP_NODE_YOHANN"),
    os.environ.get("IP_NODE_JULIEN"),
]

myUrl = f"http://{os.environ.get('MYLOCALIP')}:5000"


def broadcast_block(block: Block):
    bc = BlockSchema()
    json_block_dict = {"url": myUrl, "block": bc.dump(block)}
    print(json_block_dict)
    for host in known_hosts:
        if host != myUrl[7:-5]:
            requests.post(
                f"http://{host}:5000/blocks/updateblock",
                json.dumps(json_block_dict),
                headers={"Content-Type": "application/json"},
            )


def broadcast_transaction(signed_transaction: SignedTransaction):
    signed_transaction_schema = SignedTransactionSchema()
    signed_transaction_json = signed_transaction_schema.dumps(signed_transaction)
    for host in known_hosts:
        if host != myUrl[7:-5]:
            requests.post(
                f"http://{host}:5000/transactions/add",
                signed_transaction_json,
                headers={"Content-Type": "application/json"},
            )
