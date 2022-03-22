import json

import requests

from common.models import Block, SignedTransaction
from common.schemas import BlockSchema, SignedTransactionSchema
from common.ips import get_all_ips, get_my_ip

known_hosts = get_all_ips()
myIp = get_my_ip()
myUrl = f"http://{myIp}:5000"


def broadcast_block(block: Block):
    json_block_dict = {"url": myUrl, "block": BlockSchema.dump(block)}
    print(f"Broacasting block {block.hash()}")
    for host in known_hosts:
        if host != myIp:
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
    for host in known_hosts:
        if host != myIp:
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
