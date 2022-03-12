import json
import hashlib

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Transaction:
    uuid: str
    sender: str
    receiver: str
    amount: float
    fees: float = 0


@dataclass
class SignedTransaction:
    transaction: Transaction
    signature: str

    def __hash__(self):
        signedTxString = str(self.transaction) + str(self.signature)
        hasher = hashlib.sha256()
        hasher.update(signedTxString.encode("utf-8"))
        hasher.digest()
        return int(hasher.hexdigest(), 16)


@dataclass
class Block:
    height: int
    prev_hash: Optional[str] = ""
    signed_transactions: List[SignedTransaction] = field(default_factory=list)
    nounce: int = 0
    next_blocks: List["Block"] = field(default_factory=list)

    def __str__(self):
        return json.dumps(self.__dict__)
