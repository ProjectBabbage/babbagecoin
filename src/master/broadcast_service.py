import os
import requests

from src.common.models import Block
from src.common.schemas import BlockSchema

known_hosts = [
    "192.168.0.15",
    # "192.168.0.19",
    # "192.168.0.20",
    # "192.168.0.21",
]

url = os.environ.get("MYLOCALIP")


def broadcast_block(block: Block):
    for host in known_hosts:
        bc = BlockSchema()
        json_block_dict = {"url": url, "block": bc.dump(block)}
        requests.post(
            f"{url}/blocks/updateblock",
            json_block_dict,
            headers={"Content-Type": "application/json"},
        )
