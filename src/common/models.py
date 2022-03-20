import hashlib

from dataclasses import dataclass, field
from typing import List, Optional
from cryptography.hazmat.backends.openssl.rsa import RSAPublicKey
from cryptography.hazmat.primitives import serialization

MINING_REWARD_ADDRESS = "REWARD"


@dataclass
class PubKey:
    pub_key: RSAPublicKey

    def hash(self):
        if self.pub_key == MINING_REWARD_ADDRESS:
            return self.pub_key

        encoded_key = self.pub_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
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
        hasher = hashlib.sha256()
        hasher.update(self.uuid.encode("utf-8"))
        hasher.update(self.sender.hash().encode("utf-8"))
        hasher.update(self.receiver.hash().encode("utf-8"))
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
        signedTxString = str(self.transaction) + str(self.signature)
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
    prev_hash: Optional[str] = ""
    signed_transactions: List[SignedTransaction] = field(default_factory=list)
    nounce: int = 0
    next_blocks: List["Block"] = field(default_factory=list)  # TODO: not up to date !!!

    def hash(self):
        if self.height == 0:
            return ""

        hasher = hashlib.sha256()
        hasher.update(self.prev_hash.encode("utf-8"))
        for transaction in self.signed_transactions:
            hasher.update(transaction.signature.encode("utf-8"))
        hasher.update(f"{self.nounce}".encode("utf-8"))
        return hasher.hexdigest()

    def __str__(self):
        return f"""BLOCK(height: {self.height}, prev: {self.prev_hash},
        nounce: {self.nounce}, SignedTransactions{self.signed_transactions})"""

    def html(self):
        prev = self.prev_hash[:20]
        str_stx = ""
        for tx in self.signed_transactions:
            str_stx += f"<li>{tx.html()}</li>"

        return f"""<div style='border:1px solid black; padding:5px; margin:5px;'>
        <b>height</b>: {self.height}, <b>prev</b>: {prev}, <b>nounce</b>: {self.nounce},<br>
        <b>signed transactions</b>: <ul style='margin:0px'>{str_stx}</ul>
        </div>"""
