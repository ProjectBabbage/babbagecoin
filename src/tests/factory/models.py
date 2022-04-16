import uuid
from common.models import PubKey, SignedTransaction, Transaction, Block
from common.wallet import Wallet


def make_pubkey(private_key_filepath: str) -> PubKey:
    return Wallet.load_from_file(private_key_filepath).get_public_key()


def make_tx(sender: PubKey, receiver: PubKey, amount=5, fees=0.1):
    return Transaction(
        uuid=str(uuid.uuid4()), sender=sender, receiver=receiver, amount=amount, fees=fees
    )


def make_stx(private_key_filepath, sender, receiver, amount=5, fees=0.1):
    tx = make_tx(sender, receiver, amount, fees)
    signature = Wallet.load_from_file(private_key_filepath).sign(tx)
    return SignedTransaction(tx, signature)


def make_block(height: int, prev_hash: str, stx: list, next_blocks: list):
    return Block(
        height=height,
        prev_hash=prev_hash,
        signed_transactions=stx,
        nonce=10,
        next_blocks=next_blocks,
    )
