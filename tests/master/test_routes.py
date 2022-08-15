from babbagecoin.common.schemas import BlockSchema
from babbagecoin.master.blockchain_service import genesis, block_tbl
from tests.helpers.models import user1


# test_client is a pytest fixture (defined in conftest.py)
def test_get_working_block(test_client):
    response = test_client.get("/blocks/working_block")
    working_block = BlockSchema.loads(response.data.decode())
    assert working_block.nonce == 0
    assert len(working_block.signed_transactions) == 1


def test_receive_mined_block_from_miner(test_client, monkeypatch):
    monkeypatch.setattr("babbagecoin.master.routes.broadcast_block", lambda b: None)
    # block is mined instantly:
    monkeypatch.setattr("babbagecoin.master.blockchain_service.is_block_hash_valid", lambda b: True)

    b = user1.mine_new_block_after(genesis)
    response = test_client.post("/blocks/minedblock", json=BlockSchema.dump(b))

    assert response.data == b"ok"
    assert len(block_tbl[b.hash()].signed_transactions) == 1
