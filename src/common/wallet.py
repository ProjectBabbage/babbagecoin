import os
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.backends.openssl.rsa import RSAPublicKey
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from src.common.models import Transaction, SignedTransaction
from src.common.schemas import TransactionSchema


class Wallet:
    def __init__(self):
        if os.path.isfile(".keys"):
            # we read the alrdy generated keys
            with open(".keys", "rb") as fkeys:
                self.private_key = load_pem_private_key(fkeys.read(), password=None)
        else:
            self.private_key = rsa.generate_private_key(
                public_exponent=65537, key_size=512
            )
            with open(".keys", "wb") as target_file:
                target_file.write(self.decode_private_key())

    def decode_public_key(self):
        return self.private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

    def decode_private_key(self):
        return self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

    def sign(self, transaction: Transaction) -> SignedTransaction:
        tx_schema = TransactionSchema()
        tx_json = tx_schema.dumps(transaction)

        signature = self.private_key.sign(
            tx_json.encode("utf-8"),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256(),
        )
        return SignedTransaction(transaction, signature)

    def verify_signature(
        self, signature: str, signed_transaction: str, pub_key: RSAPublicKey
    ) -> bool:
        try:
            pub_key.verify(
                signature.encode("utf-8"),
                signed_transaction,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            )
            return True
        except InvalidSignature:
            return False


if __name__ == "__main__":
    w = Wallet()
    # print(w.decode_public())
    # print(w.decode_private())
    tx = Transaction("sldk", "sender", "slkdl", 0.1)
    print(w.sign(tx))