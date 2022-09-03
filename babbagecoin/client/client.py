import requests
import uuid
from argparse import ArgumentParser
from babbagecoin.common.models import Transaction, SignedTransaction
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

    def __init__(self, load_from_file=True):
        self.wallet = Wallet()

    def send_transaction(self, receiver: str, amount: float, fees: float):
        print(f"Sending {amount} to {receiver} with fees {fees}")
        tx = Transaction(
            uuid=str(uuid.uuid4()),
            sender=self.wallet.get_public_key(),
            receiver=receiver,
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
