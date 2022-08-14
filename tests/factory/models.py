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
from babbagecoin.common.block_service import set_difficulty, is_block_hash_valid

set_difficulty(1000)


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
    block = Block(
        height=height,
        prev_hash=prev_hash,
        signed_transactions=stx,
        nonce=0,
        next_blocks=next_blocks,
    )
    while not is_block_hash_valid(block):
        block.nonce += 1

    return block


def make_block_with_reward(prev_hash: str, height=1, miner="USER1", stx=[], next_blocks=[]):
    reward_tx = make_stx(MINING_REWARD_ADDRESS, miner)
    return make_block(prev_hash, height, [reward_tx] + stx, next_blocks)


def make_reward_block(for_user="USER1"):
    """A block with only the reward transaction."""
    return make_block_with_reward(prev_hash=genesis.hash(), miner=for_user)
