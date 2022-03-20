from common.models import Block
from master.transaction_service import (
    add_signed_transactions_from_old_block,
    remove_signed_transactions_from_valid_block,
    get_reward_transaction,
    mem_pool,
)

hash_dict = {}
genesis: Block = Block(height=0)
hash_dict[genesis.hash()] = genesis
current: Block = genesis


def update_hash_dict_all(block):
    hash_dict[block.hash()] = block
    for b in block.next_blocks:
        update_hash_dict_all(b["block"])


def update_blockchain(block: Block, leaf: Block):
    global current
    if block.prev_hash in hash_dict:
        update_hash_dict_all(block)
        prev_block = hash_dict[block.prev_hash]
        prev_block.next_blocks.append({"hash": block.hash(), "block": block})
        if leaf.height > current.height:
            # update mempool
            # add (non reward) transactions of old branch to the mempool
            b = current
            while b.hash() != block.prev_hash:
                add_signed_transactions_from_old_block(mem_pool, b)
                b = hash_dict[b.prev_hash]
            # remove transactions from the new branch
            b = leaf
            while b.hash() != block.prev_hash:
                remove_signed_transactions_from_valid_block(mem_pool, b)
                b = hash_dict[b.prev_hash]
            # change current to be the new leaf
            current = leaf
            print(f"Changing current: {current.hash()}")
    else:
        raise Exception("Does not connect to our blockchain")


def get_current() -> Block:
    global current
    return current


def build_next_block_from_current() -> Block:
    global current
    rewardTransaction = get_reward_transaction()
    new_block = Block(
        height=current.height + 1,
        prev_hash=current.hash(),
        signed_transactions=[
            rewardTransaction,
        ],
    )

    return new_block
