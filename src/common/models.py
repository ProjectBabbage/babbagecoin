import hashlib

from dataclasses import dataclass, field
from typing import List, Optional
from cryptography.hazmat.backends.openssl.rsa import RSAPublicKey
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key

MINING_REWARD_ADDRESS = "BABBAGE"


@dataclass
class PubKey:
    rsa_pub_key: RSAPublicKey or str

    @staticmethod
    def load_from_bytes(b: bytes):
        return PubKey(load_pem_public_key(b))

    def dump(self) -> bytes:
        if self.rsa_pub_key == MINING_REWARD_ADDRESS:
            return MINING_REWARD_ADDRESS.encode("utf-8")
        return self.rsa_pub_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

    def dumps(self) -> str:
        return self.dump().decode("utf-8")

    def hash(self) -> str:
        if self.rsa_pub_key == MINING_REWARD_ADDRESS:
            return MINING_REWARD_ADDRESS
        encoded_key = self.dump()
        hasher = hashlib.sha256()
        hasher.update(encoded_key)
        return hasher.hexdigest()

    def __str__(self):
        return self.hash()


@dataclass
class Transaction:
    uuid: str
    sender: PubKey
    receiver: PubKey
    amount: float
    fees: float = 0

    def hash(self):
        if self.sender.rsa_pub_key == MINING_REWARD_ADDRESS:
            return MINING_REWARD_ADDRESS
        hasher = hashlib.sha256()
        hasher.update(self.uuid.encode("utf-8"))
        hasher.update(self.sender.dump())
        hasher.update(self.receiver.dump())
        hasher.update(str(self.amount).encode("utf-8"))
        hasher.update(str(self.fees).encode("utf-8"))
        return hasher.hexdigest()

    def __str__(self):
        uuid = self.uuid[:4]
        sender = str(self.sender)[:8]
        receiver = str(self.receiver)[:8]
        amount = str(self.amount)
        fees = str(self.fees)
        return (
            f"uuid: {uuid}, sender: {sender}, receiver: {receiver}, amount: {amount}, fees: {fees}"
        )


@dataclass
class SignedTransaction:
    transaction: Transaction
    signature: str

    def hash(self):
        signedTxString = self.transaction.hash() + self.signature
        hasher = hashlib.sha256()
        hasher.update(signedTxString.encode("utf-8"))
        return hasher.hexdigest()

    def __hash__(self):
        return int(self.hash(), 16)

    def __str__(self):
        return f"stx({self.transaction})"

    def html(self):
        return f"{self.transaction}"


@dataclass
class Block:
    height: int
    prev_hash: Optional[str] = None
    # Invariant: the first transaction should be the reward transaction for mining the block
    signed_transactions: List[SignedTransaction] = field(default_factory=list)
    nonce: int = 0
    # Invariant: following the first element of next_blocks should lead to head
    next_blocks: List["Block"] = field(default_factory=list)
    _hash: Optional[str] = None

    def hash(self, recompute=False):
        if not self._hash or recompute:
            if self.height == 0:
                self._hash = ""
            else:
                hasher = hashlib.sha256()
                hasher.update(self.prev_hash.encode("utf-8"))
                for transaction in self.signed_transactions:
                    hasher.update(transaction.signature.encode("utf-8"))
                hasher.update(f"{self.nonce}".encode("utf-8"))
                self._hash = hasher.hexdigest()
        return self._hash

    def __str__(self):
        return f"""BLOCK(height: {self.height}, prev: {self.prev_hash},
        nonce: {self.nonce}, SignedTransactions{self.signed_transactions})"""

    def html(self):
        hash = self.hash()[:20]
        str_stx = ""
        for tx in self.signed_transactions:
            str_stx += f"<li>{tx.html()}</li>"

        return f"""<div style='border:1px solid black; padding:5px; margin:5px;'>
        <b>height</b>: {self.height}, <b>hash</b>: {hash}, <b>nonce</b>: {self.nonce},<br>
        <b>signed transactions</b>: <ul style='margin:0px'>{str_stx}</ul>
        </div>"""
