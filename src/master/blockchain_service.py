from common.exceptions import (
    DuplicatedTransaction,
    InvalidBlockHash,
    InvalidBlockHeight,
    InvalidSignatureForTransaction,
    RewardTransactionNotUnique,
    BadRewardTransaction,
)
from common.models import Block, MINING_REWARD_AMOUNT, MINING_REWARD_ADDRESS
from common.block_service import is_block_hash_valid
from common.wallet import Wallet
from master.transaction_service import (
    refresh_transactions_from_old_block,
    refresh_transactions_from_new_block,
    get_reward_transaction,
    validated_transactions,
)

block_tbl = {}  # map from hash to block
genesis: Block = Block(prev_hash=None, height=0)
block_tbl[genesis.hash()] = genesis
head: Block = genesis


def update_block_tbl_from(block):
    block_tbl[block.hash()] = block
    for b in block.next_blocks:
        update_block_tbl_from(b)


def remove_block_tbl_from(block):
    block_tbl.pop(block.hash())
    for b in block.next_blocks:
        remove_block_tbl_from(b)


def find_common_ancestor_of(leaf1, leaf2):
    if leaf1.height < leaf2.height:
        temp = leaf2
        leaf2 = leaf1
        leaf1 = temp
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


def sane_from(start: Block, starting_height: int):
    """
    Run verify_block on each block from start.
    Returns False if a unconsistency is detected:
    - InvalidBlockHash: the block hash doesn't match the required difficulty
    - BadRewardTransaction: the reward transaction as bad amount or bad address
    - RewardTransactionNotUnique: the reward transaction address appears after the first tx
    - InvalidSignature: the signature for a stx is incorrect
    - DuplicatedTransaction: the same transaction appeared twice in the blocks
    """
    seen_txs = set()

    def verify_block(block: Block, expected_height: int):
        if block.height != expected_height:
            raise InvalidBlockHeight(
                f"Expected height {expected_height}, actual height {block.height}"
            )
        if not is_block_hash_valid(block):
            raise InvalidBlockHash(f"INVALID BLOCK HASH {block.hash()}")
        for i, stx in enumerate(block.signed_transactions):
            if i == 0 and (
                stx.transaction.sender.dumps() != MINING_REWARD_ADDRESS
                or stx.transaction.amount != MINING_REWARD_AMOUNT
            ):
                raise BadRewardTransaction(f"BAD REWARD TRANSACTION {stx}")
            if i != 0 and stx.transaction.sender.dumps() == MINING_REWARD_ADDRESS:
                raise RewardTransactionNotUnique(f"REWARD TRANSACTION NOT UNIQUE {stx}")

            Wallet.verify_signature(stx)  # can raise an InvalidSignatureForTransaction

            if stx in seen_txs:
                raise DuplicatedTransaction(f"DUPLICATED TRANSACTION {stx}")
            seen_txs.add(stx)

    try:
        b = start
        expected_height = starting_height
        verify_block(b, expected_height)
        while len(b.next_blocks) != 0:
            b = b.next_blocks[0]
            expected_height += 1
            verify_block(b, expected_height)
        return True
    except (
        InvalidBlockHash,
        InvalidBlockHeight,
        BadRewardTransaction,
        RewardTransactionNotUnique,
        InvalidSignatureForTransaction,
        DuplicatedTransaction,
    ) as e:
        print(e)
        return False


def refresh_transactions_switch(start: Block, ancestor: Block, end: Block):
    # take into account transactions of the old branch start
    b = start
    while b.hash() != ancestor.hash():
        refresh_transactions_from_old_block(b)
        b = block_tbl[b.prev_hash]
    # take into account transactions from the new branch end
    b = end
    while b.hash() != ancestor.hash():
        refresh_transactions_from_new_block(b)
        b = block_tbl[b.prev_hash]


def update_blockchain(anchor: Block, leaf: Block):
    """
    ancestor                      head
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
    anchor_prev = block_tbl[anchor.prev_hash]
    if leaf.height > head.height and sane_from(anchor, anchor_prev.height + 1):
        update_block_tbl_from(anchor)
        anchor_prev.next_blocks.append(anchor)
        ancestor = find_common_ancestor_of(leaf, head)
        refresh_transactions_switch(head, ancestor, anchor_prev)
        b = anchor
        while True:
            excess_transactions = refresh_transactions_from_new_block(b)
            if b.hash() == leaf.hash() or excess_transactions != set():
                break
            b = b.next_blocks[0]
        if excess_transactions == set():
            # we want to keep the invariant on next_blocks
            make_primary_between(ancestor, anchor)
            # change head to be the new leaf
            head = leaf
            print(f"Changing head to {head.hash()}")
        else:
            refresh_transactions_switch(b, ancestor, head)
            for stx in excess_transactions:
                validated_transactions.add(stx)
            anchor_prev.next_blocks.pop()
            remove_block_tbl_from(anchor)
            print("Discarding new blocks due to a transaction already validated")
    """
    Verification of a transaction already validated (b) ending up in rejecting the incoming blocks:

    ancestor            anchor    leaf                      │
     ┌───┐    ┌───┐     ┌───┐     ┌───┐          ┌───┐    ┌─▼─┐     ┌───┐     ┌───┐
     │ b │    │ f │     │ a │     │ c │          │ b │    │ f │     │ a │     │ c │
     │ e ├────┤   │     │ b ├─────┤ d │          │ e ├────┤   │     │ b ├─────┤ d │
     └──┬┘    └───┘     └───┘     └───┘          └──┬┘    └───┘     └───┘     └───┘
        │              head                         │
        │     ┌───┐   ┌───┐                         │     ┌───┐   ┌───┐
        └─────┤ r ├───┤ x │                         └─────┤ r ├───┤ x │
              │ t │   │ y │                               │ t │   │ y │
              └───┘   └─▲─┘            ────────►          └───┘   └───┘
                        │

         validated     mempool                       validated     mempool
         ┌─────┐       ┌─────┐                       ┌─────┐       ┌─────┐
         │     │       │     │                       │     │       │     │
         │  b  │       │  a  │                       │  b  │       │  a  │
         │  e  │       │  c  │                       │  e  │       │  c  │
         │  r  │       │  f  │                       │  f  │       │     │
         │  t  │       │     │                       │     │       │  r  │
         │  x  │       │     │                       │     │       │  t  │
         │  y  │       │     │                       │     │       │  x  │
         │     │       │     │                       │     │       │  y  │
         └─────┘       └─────┘                       └─────┘       └─────┘
                                                                │
                                                                │
                                                                ▼
                                                                      │
     ┌───┐    ┌───┐                              ┌───┐    ┌───┐     ┌─▼─┐     ┌───┐
     │ b │    │ f │                              │ b │    │ f │     │ a │     │ c │
     │ e ├────┤   │                              │ e ├────┤   │     │ b ├─────┤ d │
     └──┬┘    └───┘                              └──┬┘    └───┘     └───┘     └───┘
        │                                           │
        │     ┌───┐   ┌───┐                         │     ┌───┐   ┌───┐
        └─────┤ r ├───┤ x │                         └─────┤ r ├───┤ x │
              │ t │   │ y │            ◄────────          │ t │   │ y │
              └───┘   └─▲─┘                               └───┘   └───┘
                        │

         validated     mempool                       validated     mempool     excess
         ┌─────┐       ┌─────┐                       ┌─────┐       ┌─────┐     ┌─────┐
         │     │       │     │                       │     │       │     │     │     │
         │  b  │       │  a  │                       │  b  │       │     │     │  b  │
         │  e  │       │  c  │                       │  e  │       │  c  │     │     │
         │  r  │       │  f  │                       │  f  │       │     │     │     │
         │  t  │       │     │                       │  a  │       │  r  │     │     │
         │  x  │       │     │                       │     │       │  t  │     │     │
         │  y  │       │     │                       │     │       │  x  │     │     │
         │     │       │     │                       │     │       │  y  │     │     │
         └─────┘       └─────┘                       └─────┘       └─────┘     └─────┘

    """


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
