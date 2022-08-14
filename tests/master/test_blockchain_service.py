from tests.factory.models import make_reward_block, make_block_with_reward
from babbagecoin.master.blockchain_service import update_blockchain, make_primary_between


def test_create_three_blocks():
    block1 = make_reward_block()
    block2 = make_block_with_reward(block1.hash(), height=2, miner="USER2")
    make_primary_between(block1, block2)
    block3 = make_block_with_reward(block2.hash(), height=3)
    make_primary_between(block2, block3)
    update_blockchain(block1, block3)
