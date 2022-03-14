from common.models import Block
from common.schemas import BlockSchema
from master.transaction_service import (
    add_signed_transactions_from_old_block,
    remove_signed_transactions_from_valid_block,
    forge_reward_transaction,
    get_reward_transaction,
    mem_pool,
)

hash_dict = {}
genesis: Block = Block(height=0)
hash_dict[genesis.hash()] = genesis
current: Block = genesis


def update_blockchain(block: Block, leaf: Block):
    global current
    if block.prev_hash in hash_dict:
        prev_block = hash_dict[block.prev_hash]
        prev_block.next_blocks.append({"hash": block.hash(), "block": block})
        update_hash_dict_all(block)
        if leaf.height > current.height:
            current = leaf
            block_schema = BlockSchema()
            current_block = block_schema.dumps(current)
            print(f"Changing current: {current_block}")

        # update mempool
        # add transactions of old branch to the mempool
        b = current
        while b.prev_hash != block.prev_hash:
            add_signed_transactions_from_old_block(mem_pool, b)
            b = hash_dict[b.prev_hash]
        # remove transaction from the new current branch
        b = leaf
        while b.height != block.height:
            remove_signed_transactions_from_valid_block(mem_pool, b)
            b = hash_dict[b.prev_hash]
            if b.height == block.height:
                remove_signed_transactions_from_valid_block(mem_pool, b)


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


def update_hash_dict_all(block):
    hash_dict[block.hash()] = block
    for b in block.next_blocks:
        update_hash_dict_all(b["block"])
