from tests.helpers.models import make_tx, make_reward_stx, make_block
from tests.helpers.users import user1, user2
from babbagecoin.master.transaction_service import get_validated_transactions, get_mem_pool
from babbagecoin.master.blockchain_service import genesis, update_blockchain, get_head
from babbagecoin.common.models import (
    PubKey,
    SignedTransaction,
    Block,
    MINING_REWARD_AMOUNT,
    MINING_REWARD_ADDRESS,
)


def test_create_three_blocks():
    block1 = user1.mine_new_block_after(genesis)
    block2 = user2.mine_new_block_after(block1)
    block3 = user1.mine_new_block_after(block2)

    update_blockchain(block1, block3)

    assert get_head().height == 3
    assert user1.balance() == 2 * MINING_REWARD_AMOUNT
    assert user2.balance() == MINING_REWARD_AMOUNT


def test_tx_fees():
    user1.cheat_balance(MINING_REWARD_AMOUNT)
    amount = MINING_REWARD_AMOUNT / 5
    fees = amount / 2
    tx1 = user1.new_transaction(user2, amount, fees)
    block = user2.mine_new_block_after(genesis, stxs=[tx1])

    update_blockchain(block, block)

    assert user1.balance() == MINING_REWARD_AMOUNT - amount - fees
    assert user2.balance() == MINING_REWARD_AMOUNT + amount + fees


def test_tx_fees_from_self():
    user1.cheat_balance(MINING_REWARD_AMOUNT)
    amount = MINING_REWARD_AMOUNT / 5
    fees = amount / 2
    tx1 = user1.new_transaction(user2, amount, fees)
    # user1 mines his transaction, so he will essentially not pay the fees
    block = user1.mine_new_block_after(genesis, stxs=[tx1])

    update_blockchain(block, block)

    assert user1.balance() == 2 * MINING_REWARD_AMOUNT - amount
    assert user2.balance() == amount


def test_duplicated_tx():
    user1.cheat_balance(MINING_REWARD_AMOUNT)

    amount = MINING_REWARD_AMOUNT / 5
    fees = amount / 2
    tx1 = user1.new_transaction(user2, amount, fees)
    block1 = user2.mine_new_block_after(genesis, stxs=[tx1])
    block2 = user2.mine_new_block_after(block1, stxs=[tx1])

    # does not accept blocks with duplicated tx
    update_blockchain(block1, block2)
    assert get_head() == genesis

    block3 = user2.mine_new_block_after(block2)

    # even if there are some innocent blocks after
    update_blockchain(block1, block3)
    assert get_head() == genesis


def test_balances_reverted():
    user1.cheat_balance(MINING_REWARD_AMOUNT)
    amount = 2 * MINING_REWARD_AMOUNT
    tx1 = user1.new_transaction(
        user2, amount
    )  # transaction not taken into account: insufficient funds
    block1 = user2.mine_new_block_after(genesis, stxs=[tx1])
    update_blockchain(block1, block1)
    assert get_head().height == 1
    assert user1.balance() == MINING_REWARD_AMOUNT
    assert user2.balance() == MINING_REWARD_AMOUNT


def test_height_not_valid():
    block1 = user1.mine_new_block_after(genesis)
    update_blockchain(block1, block1)
    assert get_head() == block1
    block2 = user2.mine_new_block_after(block1, height=3)  # height should be 2
    update_blockchain(block2, block2)
    assert get_head() == block1


def test_prev_hash_not_valid():
    block1 = user1.mine_new_block_after(genesis)
    update_blockchain(block1, block1)

    reward_stx = make_reward_stx(user2.address())
    block2 = Block(
        height=2, prev_hash="", signed_transactions=[reward_stx], nonce=0, next_blocks=[]
    )  # wrong hash of previous block
    update_blockchain(block2, block2)
    assert get_head().height == 1


def test_fork():
    user1.cheat_balance(MINING_REWARD_AMOUNT)

    amount = MINING_REWARD_AMOUNT / 5
    tx1 = user1.new_transaction(user2, amount)
    tx2 = user1.new_transaction(user2, 2 * MINING_REWARD_AMOUNT)
    block1 = user1.mine_new_block_after(genesis, stxs=[tx1, tx2])

    update_blockchain(block1, block1)
    assert user1.balance() == 2 * MINING_REWARD_AMOUNT - amount
    assert user2.balance() == amount
    assert tx1 in get_validated_transactions()
    assert tx2 in get_validated_transactions()

    block2 = user2.mine_new_block_after(genesis)
    block3 = user2.mine_new_block_after(block2)

    update_blockchain(block2, block3)  # replacing block1 with block2 and block3
    assert get_head() == block3
    assert user1.balance() == MINING_REWARD_AMOUNT
    assert user2.balance() == 2 * MINING_REWARD_AMOUNT
    assert tx1 not in get_validated_transactions()
    assert tx2 not in get_validated_transactions()
    assert tx1 in get_mem_pool()
    assert tx2 in get_mem_pool()


def test_signature_not_valid():
    user1.cheat_balance(MINING_REWARD_AMOUNT)
    amount = MINING_REWARD_AMOUNT / 5
    tx = make_tx(user1.pubkey(), user2.address(), amount, 0)
    stx = SignedTransaction(tx, "")  # transaction not correctly signed
    block = user2.mine_new_block_after(genesis, stxs=[stx])
    update_blockchain(block, block)
    assert get_head() == genesis


def test_reward_transaction_reward_not_valid():
    reward_tx = make_tx(
        PubKey(MINING_REWARD_ADDRESS), user1.address(), 2 * MINING_REWARD_AMOUNT, 0
    )  # trying to get twice as much rewards
    reward_stx = SignedTransaction(reward_tx, "")
    block = make_block(genesis, 1, [reward_stx], [])
    update_blockchain(block, block)
    assert get_head() == genesis


def test_reward_transaction_duplicate_not_valid():
    reward_stx1 = make_reward_stx(user1.address())
    reward_stx2 = make_reward_stx(user1.address())
    print(reward_stx1)
    print(reward_stx2)
    block = make_block(
        genesis, 1, [reward_stx1, reward_stx2], []
    )  # trying to get the rewards twice
    update_blockchain(block, block)
    assert get_head() == genesis


def test_no_transaction_not_valid():
    block = make_block(genesis, 1, [], [])
    update_blockchain(block, block)
    assert get_head() == genesis


def test_no_reward_transaction_not_valid():
    user1.cheat_balance(MINING_REWARD_AMOUNT)
    stx = user1.new_transaction(user2, MINING_REWARD_AMOUNT / 2)
    block = make_block(genesis, 1, [stx], [])
    update_blockchain(block, block)
    assert get_head() == genesis
