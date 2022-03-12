import hashlib
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
    prev_hash: Optional[str] = None
    signed_transactions: List[SignedTransaction] = field(default_factory=list)
    nounce: int = 0
    next_blocks: List["Block"] = field(default_factory=list)

    def __str__(self):
        return json.dumps(self.__dict__)

    def hash(self) -> str:
        m = hashlib.sha256()
        s = str(self)
        b = s.encode("utf-8")
        m.update(b)
        m.digest()
        return m.hexdigest()
