import base64
import os

from cryptography.hazmat.backends.openssl.rsa import RSAPublicKey
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.serialization import load_pem_public_key

from common.models import MINING_REWARD_ADDRESS, PubKey, Transaction, SignedTransaction


class Wallet:
    private_key: RSAPrivateKey

    def __init__(self):
        if os.path.isfile(".skey"):
            # we read the already generated keys
            with open(".skey", "rb") as fkeys:
                self.private_key = load_pem_private_key(fkeys.read(), password=None)
        else:
            self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=512)
            with open(".skey", "wb") as target_file:
                target_file.write(self.decode_private_key())

    def get_public_key(self) -> PubKey:
        return PubKey(self.private_key.public_key())

    def decode_public_key(self) -> bytes:
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

    def load_public_key(self, filepath):
        with open(filepath, "rb") as bf:
            return PubKey.load_from_bytes(bf.read())

    def sign(self, transaction: Transaction) -> SignedTransaction:
        transaction_hash = transaction.hash()
        print(type(transaction_hash), transaction_hash)

        signature = self.private_key.sign(
            transaction_hash.encode("utf-8"),
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256(),
        )
        return SignedTransaction(
            transaction=transaction,
            signature=base64.urlsafe_b64encode(signature).decode("utf-8"),
        )

    @staticmethod
    def verify_signature(signed_transaction: SignedTransaction) -> bool:

        signature = base64.urlsafe_b64encode(signed_transaction.signature.encode("utf-8"))
        transaction = signed_transaction.transaction

        if transaction.sender.dumps() != MINING_REWARD_ADDRESS:
            signed_transaction.transaction.sender.rsa_pub_key.verify(
                signature,
                transaction.hash(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            )
            # can raise an InvalidSignature
