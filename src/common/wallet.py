import base64
import hashlib
import os

from cryptography.exceptions import InvalidSignature

from cryptography.hazmat.backends.openssl.rsa import RSAPublicKey
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.serialization import load_pem_public_key

from src.common.models import PubKey, Transaction, SignedTransaction


class Wallet:
    private_key: RSAPrivateKey

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
        pub_key = ""
        with open(filepath, "rb") as pKey:
            pub_key = load_pem_public_key(pKey.read(), password=None)
        if not pub_key:
            raise Exception("No public key load")
        return pub_key

    def sign(self, transaction: Transaction) -> SignedTransaction:
        transaction_hash = transaction.hash()

        signature = self.private_key.sign(
            transaction_hash.encode("utf-8"),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256(),
        )
        return SignedTransaction(
            transaction=transaction,
            signature=base64.urlsafe_b64encode(signature).decode(),
        )

    def verify_signature(
        self, signed_transaction: SignedTransaction, pub_key: RSAPublicKey
    ) -> bool:

        signature = base64.b64decode(signed_transaction.signature.encode())
        transaction = signed_transaction.transaction
        transaction_hash = transaction.hash()
        #
        try:
            pub_key.verify(
                signature,
                transaction_hash,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            )
            return True
        except InvalidSignature:
            return False

    @staticmethod  # TODO : remove this ?
    def get_public_address(decoded_public_key):
        hasher = hashlib.sha256()
        hasher.update(decoded_public_key)
        return hasher.hexdigest()


if __name__ == "__main__":
    w = Wallet()
    # print(w.decode_public())
    # print(w.decode_private())
    tx = Transaction("sldk", "sender", "slkdl", 0.1)
    print(w.sign(tx))
