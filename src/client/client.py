import os
import requests
import uuid
from dotenv import load_dotenv
from common.wallet import Wallet
from argparse import ArgumentParser
from common.models import PubKey, Transaction, SignedTransaction
from common.schemas import SignedTransactionSchema
from common.ips import get_my_ip


parser = ArgumentParser(description="Send a transaction on babbagecoin")

parser.add_argument("receiver", type=str)
parser.add_argument("amount", type=float)
parser.add_argument("fees", type=float)


myUrl = f"http://{get_my_ip()}:5000/"


class Client:
    wallet: Wallet

    def __init__(self):
        self.wallet = Wallet()
        self.receivers = self.load_receivers()

    def load_receivers(self):
        # load public keys from file in pub_keys/ and return a dict {hash_pk: PubKey}
        address_to_pk = {}
        for filepath in os.listdir("./pub_keys"):
            pk = self.wallet.load_public_key(f"{os.getcwd()}/pub_keys/{filepath}")
            address_to_pk[str(pk)] = pk
            print(pk)
        return address_to_pk

    def send_transaction(self, receiver: str, amount: float, fees: float):
        print(f"Sending {amount} to {receiver} with fees {fees}")
        tx = Transaction(
            uuid=str(uuid.uuid4()),
            sender=self.wallet.get_public_key(),
            receiver=receiver,
            amount=amount,
            fees=fees,
        )
        signedTxSchema = SignedTransactionSchema()
        signedTx = SignedTransaction(tx, self.wallet.sign(tx))
        requests.post(
            f"{myUrl}/transactions/emit",
            signedTxSchema.dumps(signedTx),
            headers={"Content-Type": "application/json"},
        )

    # TODO
    def get_balance(self):
        # get the client balance
        pass


def run(receiver, amount, fees: float):
    c = Client()
