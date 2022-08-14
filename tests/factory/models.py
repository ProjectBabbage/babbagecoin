import uuid
from babbagecoin.common.models import (
    PubKey,
    SignedTransaction,
    Transaction,
    Block,
    MINING_REWARD_AMOUNT,
    MINING_REWARD_ADDRESS,
)
from babbagecoin.common.wallet import Wallet
from babbagecoin.master.blockchain_service import genesis


def make_pubkey(user: str) -> PubKey:
    if user == MINING_REWARD_ADDRESS:
        return PubKey(MINING_REWARD_ADDRESS)
    return Wallet.load_from_file(
        f"babbagecoin/tests/fixtures/private_keys/{user}.txt"
    ).get_public_key()


def make_tx(sender: str, receiver: str, amount=5, fees=0.1):
    if sender == MINING_REWARD_ADDRESS:
        amount = MINING_REWARD_AMOUNT
        fees = 0
    return Transaction(
        uuid=str(uuid.uuid4()),
        sender=make_pubkey(sender),
        receiver=make_pubkey(receiver),
        amount=amount,
        fees=fees,
    )


def make_stx(sender: str, receiver: str, amount=5, fees=0.1):
    tx = make_tx(sender, receiver, amount, fees)
    if sender == MINING_REWARD_ADDRESS:
        sender = receiver
    signature = Wallet.load_from_file(f"babbagecoin/tests/fixtures/private_keys/{sender}.txt").sign(
        tx
    )
    return SignedTransaction(tx, signature)


def make_block(prev_hash: str, height=1, stx=[], next_blocks=[]):
    return Block(
        height=height,
        prev_hash=prev_hash,
        signed_transactions=stx,
        nonce=0,
        next_blocks=next_blocks,
    )


def make_reward_block(for_user: str):
    """A block with only the reward transaction."""
    reward_tx = make_stx(MINING_REWARD_ADDRESS, for_user)
    b = make_block(prev_hash=genesis.hash(), stx=[reward_tx])
    return b
