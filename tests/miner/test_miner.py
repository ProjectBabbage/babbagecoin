from babbagecoin.miner.miner import BlockStore
from tests.helpers.users import user1
from babbagecoin.master.blockchain_service import genesis


def test_update_working_block(monkeypatch):
    # get_working_block()
    b = user1.mine_new_block_after(genesis)

    monkeypatch.setattr("babbagecoin.miner.miner.get_working_block", lambda: b)

    bs = BlockStore()

    assert bs.working_block is None
    assert bs.initial_hash is None

    bs.update_working_block()

    assert bs.working_block == b
    assert bs.initial_hash == b.hash()
