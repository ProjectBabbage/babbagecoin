from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends.openssl.rsa import RSAPublicKey
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from src.common.models import Transaction, SignedTransaction
from src.common.schemas import TransactionSchema


class Wallet:
    def __init__(self):
        self.public_key, self.private_key = self.generate_keys()

    def generate_keys(self):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=512)
        public_key = private_key.public_key()
        return public_key, private_key

    def decode_public(self):
        return (
            self.private_key.public_key()
            .public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
            .decode("utf-8")
        )

    def decode_private(self):
        return self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        ).decode("utf-8")

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
    print(w.decode_public())
    print(w.decode_private())
    tx = Transaction("sldk", "sender", "slkdl", 0.1)
    print(w.sign(tx))
