from unittest import TestCase
from unittest.mock import patch
from master.broadcast_service import broadcast_block
from tests.factory.models import make_block, make_stx, make_pubkey


class TestBroadcast(TestCase):
    @patch("master.broadcast_service.context")
    @patch("requests.post", return_value="")
    def test_broadcast_block(self, mock_post, mock_context):

        mock_context.myIp = "192.168.122.1"
        mock_context.myUrl = "http://192.168.122.1:5000"
        # two nodes tests
        mock_context.known_hosts = ["192.168.122.1", "192.168.122.2"]

        sender_privk_filepath = "src/tests/fixtures/private_keys/USER1.txt"
        receiver_privk_filepath = "src/tests/fixtures/private_keys/USER2.txt"
        sender = make_pubkey(sender_privk_filepath)
        receiver = make_pubkey(receiver_privk_filepath)
        stx = make_stx(sender_privk_filepath, sender, receiver)
        b = make_block(1, "prev_hash", [stx], [])

        broadcast_block(b)

        # not broadcasted to myself, only to the other node
        mock_post.assert_called_once()
