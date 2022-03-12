import os
import requests
import uuid
from dotenv import load_dotenv
from src.common.wallet import Wallet
from argparse import ArgumentParser
from src.common.models import Transaction, SignedTransaction
from src.common.schemas import TransactionSchema, SignedTransactionSchema

load_dotenv()
parser = ArgumentParser(description="Send a transaction on babbagecoin")

parser.add_argument("receiver", type=str)
parser.add_argument("amount", type=float)
parser.add_argument("fees", type=float)


myUrl = f"http://{os.environ.get('MYLOCALIP')}:5000/"


class Client:
    wallet: Wallet

    def __init__(self):
        self.wallet = Wallet()

    def send_transaction(self, receiver: str, amount: float, fees: float):
        print(f"Sending {amount} to {receiver} with fees {fees}")
        tx = Transaction(
            str(uuid.uuid4()), self.wallet.decode_public_key(), receiver, amount, fees
        )
        signedTxSchema = SignedTransactionSchema()
        signedTx = SignedTransaction(tx, self.wallet.sign(tx))
        requests.post(
            f"{myUrl}/transactions/add",
            signedTxSchema.dumps(signedTx),
            headers={"Content-Type": "application/json"},
        )


if __name__ == "__main__":
    args = parser.parse_args()
    print(args)
    client = Client()
    client.send_transaction(args.receiver, args.amount, args.fees)
