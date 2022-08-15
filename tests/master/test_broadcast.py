from unittest import TestCase
from unittest.mock import patch
from babbagecoin.master.blockchain_service import genesis
from babbagecoin.master.broadcast_service import broadcast_block, broadcast_transaction
from tests.helpers.users import user1, user2


class TestBroadcast(TestCase):
    @patch("babbagecoin.master.broadcast_service.context")
    @patch("requests.post", return_value="")
    def test_broadcast_block(self, mock_post, mock_context):

        mock_context.myIp = "192.168.122.1"
        mock_context.myUrl = "http://192.168.122.1:5000"
        # two nodes tests
        mock_context.known_nodes = ["192.168.122.1", "192.168.122.2"]

        stx = user1.new_transaction(user2)
        b = user1.mine_new_block_after(genesis, stxs=[stx])

        broadcast_block(b)

        # not broadcasted to myself, only to the other node
        mock_post.assert_called_once()

    @patch("babbagecoin.master.broadcast_service.context")
    @patch("requests.post", return_value="")
    def test_broadcast_transaction(self, mock_post, mock_context):
        mock_context.myIp = "192.168.122.1"
        mock_context.myUrl = "http://192.168.122.1:5000"
        # 3 nodes
        mock_context.known_nodes = ["192.168.122.1", "192.168.122.2", "192.168.122.3"]
        stx = user1.new_transaction(user2)
        broadcast_transaction(stx)
        assert mock_post.call_count == 2
