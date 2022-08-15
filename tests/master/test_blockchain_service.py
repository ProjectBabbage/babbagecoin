from tests.helpers.users import user1, user2
from babbagecoin.master.blockchain_service import genesis
from babbagecoin.master.blockchain_service import update_blockchain


def test_create_three_blocks():
    block1 = user1.mine_new_block_after(genesis)
    block2 = user2.mine_new_block_after(block1)
    block3 = user1.mine_new_block_after(block2)
    update_blockchain(block1, block3)
