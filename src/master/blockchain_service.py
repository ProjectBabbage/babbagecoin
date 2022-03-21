from common.models import Block
from master.transaction_service import (
    add_signed_transactions_from_old_block,
    remove_signed_transactions_from_valid_block,
    get_reward_transaction,
    mem_pool,
)

block_tbl = {}
genesis: Block = Block(height=0)
block_tbl[genesis.hash()] = genesis
current: Block = genesis


def update_block_tbl_from(block):
    block_tbl[block.hash()] = block
    for b in block.next_blocks:
        update_block_tbl_from(b)


def update_blockchain(block: Block, leaf: Block):
    global current
    if block.prev_hash in block_tbl:
        update_block_tbl_from(block)
        prev_block = block_tbl[block.prev_hash]
        if leaf.height > current.height:
            # update mempool
            # add (non reward) transactions of old branch to the mempool
            b = current
            while b.hash() != block.prev_hash:
                add_signed_transactions_from_old_block(mem_pool, b)
                b = block_tbl[b.prev_hash]
            # remove transactions from the new branch
            b = leaf
            while b.hash() != block.prev_hash:
                remove_signed_transactions_from_valid_block(mem_pool, b)
                b = block_tbl[b.prev_hash]
            # change current to be the new leaf
            current = leaf
            # we want to keep the invariant on next_blocks
            prev_block.next_blocks = [block] + prev_block.next_blocks
            print(f"Changing current: {current.hash()}")
        else:
            # we want to keep the invariant on next_blocks
            prev_block.next_blocks.append(block)

    else:
        raise Exception("Does not connect to our blockchain")


def get_current() -> Block:
    return current


def build_next_block_from_current() -> Block:
    rewardTransaction = get_reward_transaction()
    new_block = Block(
        height=current.height + 1,
        prev_hash=current.hash(),
        signed_transactions=[
            rewardTransaction,
        ],
    )
    return new_block


def delta_balance_block(address, block):
    delta = 0
    miner = block.signed_transactions[0].transaction.receiver
    for stx in block.signed_transactions:
        tx = stx.transaction
        if str(tx.receiver) == address:
            delta += tx.amount
        if str(tx.sender) == address:
            delta -= tx.amount + tx.fees
        if str(miner) == address:
            delta += tx.fees
    return delta


def compute_balance(address: str):
    if genesis.next_blocks == []:
        return 0
    b = genesis.next_blocks[0]
    amount = 0

    while b.next_blocks != []:
        amount += delta_balance_block(address, b)
        b = b.next_blocks[0]

    return amount
