import pytest
from babbagecoin.client.client import Client
from tests.factory.models import make_pubkey


@pytest.fixture()
def client(monkeypatch):
    pk_user2 = make_pubkey("USER2")
    monkeypatch.setattr(Client, "load_contacts", lambda s: {"USER2": pk_user2})
    c = Client(False)
    yield c


def test_send_transaction(client, monkeypatch):
    post_count = 0

    def mock_post(url, json, headers):
        nonlocal post_count
        post_count += 1

    monkeypatch.setattr("babbagecoin.client.client.requests.post", mock_post)
    client.send_transaction("USER2", 10, 1)

    assert post_count == 1
