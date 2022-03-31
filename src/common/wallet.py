import os

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.exceptions import InvalidSignature

from common.models import MINING_REWARD_ADDRESS, PubKey, Transaction, SignedTransaction
from common.exceptions import InvalidSignatureForTransaction


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

    def sign(self, transaction: Transaction) -> str:
        return self.private_key.sign(
            transaction.hash().encode(),
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256(),
        ).hex()

    @staticmethod
    def verify_signature(signed_transaction: SignedTransaction) -> bool:

        signature = bytes.fromhex(signed_transaction.signature)
        transaction = signed_transaction.transaction
        transaction_hash = transaction.hash().encode()

        if transaction.sender.dumps() != MINING_REWARD_ADDRESS:
            try:
                signed_transaction.transaction.sender.rsa_pub_key.verify(
                    signature,
                    transaction_hash,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH,
                    ),
                    hashes.SHA256(),
                )
            except InvalidSignature:
                raise InvalidSignatureForTransaction(
                    f"INVALID SIGNATURE {signed_transaction.signature}, for stx {signed_transaction}, of tx hash: {transaction_hash}"
                )

    @staticmethod
    def load_pub_key(filepath):
        with open(filepath, "rb") as bf:
            return PubKey.load_from_bytes(bf.read())
