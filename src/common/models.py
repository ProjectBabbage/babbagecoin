import json

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


@dataclass
class Block:
    prev_hash: Optional[str] = ""
    height: int
    signed_transactions: List[SignedTransaction] = field(default_factory=list)
    nounce: int = 0
    next_blocks: List["Block"] = field(default_factory=list)

    def __str__(self):
        return json.dumps(self.__dict__)
