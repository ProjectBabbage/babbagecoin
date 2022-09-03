from tests.helpers.users import user1, user2
from babbagecoin.master.blockchain_service import genesis, update_blockchain, get_head
from babbagecoin.common.models import MINING_REWARD_AMOUNT


def test_create_three_blocks():
    block1 = user1.mine_new_block_after(genesis)
    block2 = user2.mine_new_block_after(block1)
    block3 = user1.mine_new_block_after(block2)
    update_blockchain(block1, block3)
    assert get_head().height == 3


def test_tx_transfer():
    block1 = user1.mine_new_block_after(genesis)
    amount = MINING_REWARD_AMOUNT / 5
    fees = amount / 2
    tx1 = user1.new_transaction(user2, amount, fees)
    block2 = user2.mine_new_block_after(block1, stxs=[tx1])
    update_blockchain(block1, block2)
    assert user1.balance() == MINING_REWARD_AMOUNT - amount - fees
    assert user2.balance() == MINING_REWARD_AMOUNT + amount + fees


def test_duplicated_tx():
    block1 = user1.mine_new_block_after(genesis)
    update_blockchain(block1, block1)
    amount = MINING_REWARD_AMOUNT / 5
    fees = amount / 2
    tx1 = user1.new_transaction(user2, amount, fees)
    block2 = user2.mine_new_block_after(block1, stxs=[tx1])
    block3 = user2.mine_new_block_after(block2, stxs=[tx1])
    update_blockchain(block2, block3)
    assert get_head().height == 1
