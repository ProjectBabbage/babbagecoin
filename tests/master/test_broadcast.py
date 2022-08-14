from unittest import TestCase
from unittest.mock import patch
from babbagecoin.master.broadcast_service import broadcast_block, broadcast_transaction
from tests.factory.models import make_block, make_stx


class TestBroadcast(TestCase):
    @patch("babbagecoin.master.broadcast_service.context")
    @patch("requests.post", return_value="")
    def test_broadcast_block(self, mock_post, mock_context):

        mock_context.myIp = "192.168.122.1"
        mock_context.myUrl = "http://192.168.122.1:5000"
        # two nodes tests
        mock_context.known_nodes = ["192.168.122.1", "192.168.122.2"]

        stx = make_stx("USER1", "USER2")
        b = make_block(prev_hash="prev_hash", stx=[stx])

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
        stx = make_stx("USER1", "USER2")
        broadcast_transaction(stx)
        assert mock_post.call_count == 2
