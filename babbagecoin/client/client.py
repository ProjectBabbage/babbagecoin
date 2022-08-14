import os
import requests
import uuid
from argparse import ArgumentParser
from babbagecoin.common.models import PubKey, Transaction, SignedTransaction
from babbagecoin.common.wallet import Wallet
from babbagecoin.common.schemas import SignedTransactionSchema
from babbagecoin.common.context import NetworkContext


parser = ArgumentParser(description="Send a transaction on babbagecoin")

parser.add_argument("receiver", type=str)
parser.add_argument("amount", type=float)
parser.add_argument("fees", type=float)

context = NetworkContext()


class Client:
    wallet: Wallet
    contacts: dict[str:PubKey]

    def __init__(self, load_from_file=True):
        self.wallet = Wallet(load_from_file=load_from_file)
        self.contacts = self.load_contacts()

    def load_contacts(self):
        # load public keys from file in pub_keys/ and return a dict {hash_pk: PubKey}
        contact_name_to_pk = {}
        for filepath in os.listdir("./pub_keys"):
            absolute_filepath = f"{os.getcwd()}/pub_keys/{filepath}"
            name, pk = filepath.split(".")[0], Wallet.load_pub_key(absolute_filepath)
            contact_name_to_pk[name] = pk
        return contact_name_to_pk

    def send_transaction(self, receiver: str, amount: float, fees: float):
        print(f"Sending {amount} to {receiver} with fees {fees}")
        if receiver not in self.contacts:
            raise Exception(f"Not in contacts list: {receiver}")
        tx = Transaction(
            uuid=str(uuid.uuid4()),
            sender=self.wallet.get_public_key(),
            receiver=self.contacts[receiver],
            amount=float(amount),
            fees=float(fees),
        )

        signedTx = SignedTransaction(tx, self.wallet.sign(tx))
        try:
            requests.post(
                f"{context.myUrl}/transactions/emit",
                SignedTransactionSchema.dumps(signedTx),
                headers={"Content-Type": "application/json"},
            )
        except requests.exceptions.ConnectionError:
            print(f"Node master at {context.myUrl} is not accessible.")

    def get_balance(self):
        try:
            addr = str(self.wallet.get_public_key())
            res = requests.get(
                f"{context.myUrl}/addresses/{addr}/balance",
                headers={"Content-Type": "application/json"},
            )
            print(res.json())
        except requests.exceptions.ConnectionError:
            print(f"Node master at {context.myUrl} is not accessible.")


def check_balance():
    client = Client()
    client.get_balance()


def send_transaction(receiver, amount, fees: float):
    client = Client()
    client.send_transaction(receiver, amount, fees)
