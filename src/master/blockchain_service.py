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
head: Block = genesis


def update_block_tbl_from(block):
    block_tbl[block.hash()] = block
    for b in block.next_blocks:
        update_block_tbl_from(b)


def update_blockchain(ancestor_next: Block, leaf: Block):
    global head
    if ancestor_next.prev_hash in block_tbl:
        update_block_tbl_from(ancestor_next)
        ancestor = block_tbl[ancestor_next.prev_hash]
        if leaf.height > head.height:
            # update mempool
            # add (non reward) transactions of old branch to the mempool
            b = head
            while b.hash() != ancestor_next.prev_hash:
                add_signed_transactions_from_old_block(mem_pool, b)
                b = block_tbl[b.prev_hash]
            # remove transactions from the new branch
            b = leaf
            while b.hash() != ancestor_next.prev_hash:
                remove_signed_transactions_from_valid_block(mem_pool, b)
                b = block_tbl[b.prev_hash]
            # change head to be the new leaf
            head = leaf
            # we want to keep the invariant on next_blocks
            ancestor.next_blocks = [ancestor_next] + ancestor.next_blocks
            print(f"Changing head to {head.hash()}")
        else:
            # we want to keep the invariant on next_blocks
            ancestor.next_blocks.append(ancestor_next)

    else:
        raise Exception("Does not connect to our blockchain")


def get_head() -> Block:
    return head


def build_working_block() -> Block:
    rewardTransaction = get_reward_transaction()
    new_block = Block(
        height=head.height + 1,
        prev_hash=head.hash(),
        signed_transactions=[rewardTransaction],
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
    if not genesis.next_blocks:
        return 0
    b = genesis.next_blocks[0]
    amount = 0

    while b.next_blocks:
        amount += delta_balance_block(address, b)
        b = b.next_blocks[0]

    return amount
