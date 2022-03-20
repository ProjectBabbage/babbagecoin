import os
import requests
import uuid
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
    contacts: dict[str:PubKey]

    def __init__(self):
        self.wallet = Wallet()
        self.contacts = self.load_contacts()

    def load_contacts(self):
        # load public keys from file in pub_keys/ and return a dict {hash_pk: PubKey}
        address_to_pk = {}
        for filepath in os.listdir("./pub_keys"):
            pk = PubKey(self.wallet.load_public_key(f"{os.getcwd()}/pub_keys/{filepath}"))
            name = filepath.split(".")[0]
            address_to_pk[name] = pk
        return address_to_pk

    def send_transaction(self, receiver: str, amount: float, fees: float):
        print(f"Sending {amount} to {receiver} with fees {fees}")
        if receiver not in self.contacts:
            raise Exception(f"Not in contacts list: {receiver}")
        tx = Transaction(
            uuid=str(uuid.uuid4()),
            sender=self.wallet.get_public_key(),
            receiver=self.contacts[receiver],
            amount=amount,
            fees=fees,
        )

        signedTx = SignedTransaction(tx, self.wallet.sign(tx))
        try:

            requests.post(
                f"{myUrl}/transactions/emit",
                SignedTransactionSchema.dumps(signedTx),
                headers={"Content-Type": "application/json"},
            )
        except requests.exceptions.ConnectionError:
            print(f"Node master at {myUrl} is not accessible.")

    # TODO
    def get_balance(self):
        # Ask master for this wallet address balance
        pass


def run(receiver, amount, fees: float):
    client = Client()
    client.send_transaction(receiver, amount, fees)
