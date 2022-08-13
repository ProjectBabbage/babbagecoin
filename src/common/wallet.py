from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.exceptions import InvalidSignature

from common.models import MINING_REWARD_ADDRESS, PubKey, Transaction, SignedTransaction
from common.exceptions import InvalidSignatureForTransaction
from common.context import get_current_user


class Wallet:
    secret_key: RSAPrivateKey

    def __init__(self, load_from_file=False):
        user_skey = f"{get_current_user()}.skey"

        if load_from_file and Path(user_skey).is_file():
            # we read the already existing secret key
            self.secret_key = Wallet.load_priv_keys(user_skey)
        else:
            # or we create a new one
            self.secret_key = rsa.generate_private_key(public_exponent=65537, key_size=512)

        self.create_key_files()

    def create_key_files(self):
        """Create the <CURRENT_USER>.skey and <CURRENT_USER>.pkey files."""
        user_skey, user_pkey = f"{get_current_user()}.skey", f"{get_current_user()}.pkey"

        with open(user_skey, "wb") as skfile:
            skfile.write(self.decode_secret_key())
        with open(user_pkey, "wb") as pkfile:
            pkfile.write(self.get_public_key().dump())

    def get_public_key(self) -> PubKey:
        return PubKey(self.secret_key.public_key())

    def decode_public_key(self) -> bytes:
        return self.secret_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

    def decode_secret_key(self) -> bytes:
        return self.secret_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )

    def sign(self, transaction: Transaction) -> str:
        return self.secret_key.sign(
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
                    f"INVALID SIGNATURE {signed_transaction.signature}, for stx "
                    "{signed_transaction}, of tx hash: {transaction_hash}"
                )

    @staticmethod
    def load_pub_key(filepath):
        with open(filepath, "rb") as bf:
            return PubKey.load_from_bytes(bf.read())

    @staticmethod
    def load_from_file(filepath):
        w = Wallet()
        w.secret_key = Wallet.load_priv_keys(filepath)
        return w

    @staticmethod
    def load_priv_keys(filepath):
        with open(filepath, "rb") as fkey:
            return load_pem_private_key(fkey.read(), password=None)
