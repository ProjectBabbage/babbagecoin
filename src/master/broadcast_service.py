import json

from common.request import node_request

from common.models import Block, SignedTransaction
from common.schemas import BlockSchema, SignedTransactionSchema
from config import Config

context = Config()


def broadcast_block(block: Block):
    json_block_dict = {"url": context.myUrl, "block": BlockSchema.dump(block)}
    print(f"Broacasting block {block.hash()}")
    for host in context.known_nodes:
        if host != context.myIp:
            try:
                node_request.post(
                    f"http://{host}:5000/blocks/updateblock",
                    json.dumps(json_block_dict),
                    headers={"Content-Type": "application/json"},
                )
            except node_request.exceptions.ConnectionError:
                print(f"Cannot connect to node {host}")
            except Exception as e:
                print(f"An error occured when broadcasting the block: {e}")


def broadcast_transaction(signed_transaction: SignedTransaction):
    signed_transaction_json = SignedTransactionSchema.dumps(signed_transaction)
    print(f"Broadcasting transaction {signed_transaction.hash()}")
    for host in context.known_nodes:
        if host != context.myIp:
            try:
                node_request.post(
                    f"http://{host}:5000/transactions/add",
                    signed_transaction_json,
                    headers={"Content-Type": "application/json"},
                )
            except node_request.exceptions.ConnectionError:
                print(f"Cannot connect to node {host}")
            except Exception as e:
                print(f"Cannot broadcast transaction: {e}")
