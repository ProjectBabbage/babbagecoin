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
from babbagecoin.master.blockchain_service import make_primary_between
from babbagecoin.common.block_service import set_difficulty, is_block_hash_valid

set_difficulty(1000)


def make_tx(sender: PubKey, receiver: str, amount, fees):
    return Transaction(
        uuid=str(uuid.uuid4()),
        sender=sender,
        receiver=receiver,
        amount=amount,
        fees=fees,
    )


def make_stx(sender_wallet: Wallet, receiver: str, amount=5, fees=0):
    tx = make_tx(sender_wallet.get_public_key(), receiver, amount, fees)
    signature = sender_wallet.sign(tx)
    return SignedTransaction(tx, signature)


def make_reward_stx(receiver: str):
    tx = make_tx(PubKey(MINING_REWARD_ADDRESS), receiver, MINING_REWARD_AMOUNT)
    return SignedTransaction(tx, "")


def make_block(
    prev_block: Block, height: int, stxs: list[SignedTransaction], next_blocks: list[Block]
):
    block = Block(
        height=height,
        prev_hash=prev_block.hash(),
        signed_transactions=stxs,
        nonce=0,
        next_blocks=next_blocks,
    )
    while not is_block_hash_valid(block):
        block.nonce += 1
    make_primary_between(prev_block, block)
    return block


def make_block_with_reward(
    prev_block: Block,
    miner: str,
    height: int,
    stxs: list[SignedTransaction],
    next_blocks: list[Block],
):
    reward_stx = make_reward_stx(miner)
    return make_block(prev_block, height, [reward_stx] + stxs, next_blocks)
