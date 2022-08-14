import json

import requests

from babbagecoin.common.models import Block, SignedTransaction
from babbagecoin.common.schemas import BlockSchema, SignedTransactionSchema
from babbagecoin.common.context import NetworkContext

context = NetworkContext()


def broadcast_block(block: Block):
    json_block_dict = {"url": context.myUrl, "block": BlockSchema.dump(block)}
    print(f"Broacasting block {block.hash()}")
    for host in context.known_nodes:
        if host != context.myIp:
            try:
                requests.post(
                    f"http://{host}:5000/blocks/updateblock",
                    json.dumps(json_block_dict),
                    headers={"Content-Type": "application/json"},
                )
            except requests.exceptions.ConnectionError:
                print(f"Cannot connect to node {host}")
            except Exception as e:
                print(f"An error occured when broadcasting the block: {e}")


def broadcast_transaction(signed_transaction: SignedTransaction):
    signed_transaction_json = SignedTransactionSchema.dumps(signed_transaction)
    print(f"Broadcasting transaction {signed_transaction.hash()}")
    for host in context.known_nodes:
        if host != context.myIp:
            try:
                requests.post(
                    f"http://{host}:5000/transactions/add",
                    signed_transaction_json,
                    headers={"Content-Type": "application/json"},
                )
            except requests.exceptions.ConnectionError:
                print(f"Cannot connect to node {host}")
            except Exception as e:
                print(f"Cannot broadcast transaction: {e}")
