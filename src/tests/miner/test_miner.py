from miner.miner import BlockStore
from tests.factory.models import make_reward_block


def test_update_working_block(monkeypatch):
    # get_working_block()
    b = make_reward_block(for_user="USER1")

    monkeypatch.setattr("miner.miner.get_working_block", lambda: b)

    bs = BlockStore()

    assert bs.working_block is None
    assert bs.initial_hash is None

    bs.update_working_block()

    assert bs.working_block == b
    assert bs.initial_hash == b.hash()
