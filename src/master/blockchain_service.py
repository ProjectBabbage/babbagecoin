from common.models import Block
from master.transaction_service import (
    add_signed_transactions_from_old_block,
    remove_signed_transactions_from_valid_block,
    get_reward_transaction,
    mem_pool,
)

block_tbl = {}
genesis: Block = Block(prev_hash=None, height=0)
block_tbl[genesis.hash()] = genesis
head: Block = genesis


def update_block_tbl_from(block):
    block_tbl[block.hash()] = block
    for b in block.next_blocks:
        update_block_tbl_from(b)


def find_common_ancestor_of(leaf1, leaf2):
    # requires leaf1.height > leaf2.height
    cursor1 = leaf1
    while cursor1.height > leaf2.height + 1:
        cursor1 = block_tbl[cursor1.prev_hash]
    cursor2 = leaf2
    while cursor1.prev_hash != cursor2.hash():
        cursor1 = block_tbl[cursor1.prev_hash]
        cursor2 = block_tbl[cursor2.prev_hash]
    return cursor2


def make_primary_between(start, end):
    """
      start
      ┌───┐   ┌───┐                       ┌───┐   ┌───┐  ┌───┐
    ──┤ s ├─┬─┤ y │                     ──┤ s ├─┬─┤ x ├──┤ e │
      └───┘ │ └───┘                       └───┘ │ └───┘  └───┘
            │               ─────────►          │
            │         end                       │
            │ ┌───┐  ┌───┐                      │ ┌───┐
            └─┤ x ├──┤ e │                      └─┤ y │
              └───┘  └───┘                        └───┘
    """
    if start.hash() != end.hash():
        prev = block_tbl[end.prev_hash]
        i = 0
        for j, e in enumerate(prev.next_blocks):
            if e.hash() == end.hash():
                i = j
                break
        temp = prev.next_blocks[0]
        prev.next_blocks[0] = end
        prev.next_blocks[i] = temp
        make_primary_between(start, prev)


def update_blockchain(anchor: Block, leaf: Block):
    """
                                 head
     ┌───┐   ┌───┐               ┌───┐
     │ a ├─┬─┤ b ├───────────────┤ c │
     └───┘ │ └───┘               └───┘
           │
           │ ┌───┐   ┌───┐
           └─┤ d ├─┬─┤ e │
             └───┘ │ └───┘
                   │         anchor        leaf
                   │ ┌───┐   ┌───┐         ┌───┐
                   └─┤ f │   │ g ├─────────┤ h │
                     └───┘   └───┘         └───┘
                  │
                  │
                  ▼
    ancestor                 anchor      head = leaf
     ┌───┐   ┌───┐   ┌───┐   ┌───┐         ┌───┐
     │ a ├─┬─┤ d ├─┬─┤ f ├───┤ g ├─────────┤ h │
     └───┘ │ └───┘ │ └───┘   └───┘         └───┘
           │       │
           │       │ ┌───┐
           │       └─┤ e │
           │         └───┘
           │
           │ ┌───┐               ┌───┐
           └─┤ b ├───────────────┤ c │
             └───┘               └───┘
    """
    global head
    if anchor.prev_hash not in block_tbl:
        raise Exception("Does not connect to our blockchain")
    # TODO: verify chain between anchor and leaf
    if leaf.height > head.height:
        update_block_tbl_from(anchor)
        anchor_prev = block_tbl[anchor.prev_hash]
        anchor_prev.next_blocks.append(anchor)
        ancestor = find_common_ancestor_of(leaf, head)
        make_primary_between(ancestor, leaf)
        # update mempool
        # add (non reward) transactions of old branch to the mempool
        b = head
        while b.hash() != ancestor.hash():
            add_signed_transactions_from_old_block(mem_pool, b)
            b = block_tbl[b.prev_hash]
        # remove transactions from the new branch
        b = leaf
        while b.hash() != ancestor.hash():
            remove_signed_transactions_from_valid_block(mem_pool, b)
            b = block_tbl[b.prev_hash]
        # change head to be the new leaf
        head = leaf
        # we want to keep the invariant on next_blocks
        print(f"Changing head to {head.hash()}")
    else:
        print("Discarding received block")


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
