from pathlib import Path

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.exceptions import InvalidSignature

from babbagecoin.common.models import MINING_REWARD_ADDRESS, PubKey, Transaction, SignedTransaction
from babbagecoin.common.exceptions import InvalidSignatureForTransaction
from babbagecoin.common.context import get_current_user


class Wallet:
    private_key: RSAPrivateKey

    def __init__(self, load_from_file=True, save_to_file=True):
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=512)

        user_privk_filepath = f"private.key.{get_current_user()}"
        if load_from_file and Path(user_privk_filepath).is_file():
            self.private_key = Wallet.load_priv_keys(user_privk_filepath)
            print(f"Found {user_privk_filepath}, using it.")
        if save_to_file and not Path(user_privk_filepath).is_file():
            self.save_files()
            print("Saving key files.")

    def save_files(self):
        """Create the private.key.<CURRENT_USER> and public.key.<CURRENT_USER> files."""
        user_private = f"private.key.{get_current_user()}"
        user_public = f"public.key.{get_current_user()}"
        with open(user_private, "wb") as priv:
            priv.write(self.decode_private_key())
        with open(user_public, "wb") as pub:
            pub.write(self.decode_public_key())

    def get_public_key(self) -> PubKey:
        return PubKey(self.private_key.public_key())

    def decode_public_key(self) -> bytes:
        return self.private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

    def decode_private_key(self) -> bytes:
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
                    f"INVALID SIGNATURE {signed_transaction.signature}, for stx "
                    "{signed_transaction}, of tx hash: {transaction_hash}"
                )

    @staticmethod
    def load_pub_key(filepath):
        with open(filepath, "rb") as bf:
            return PubKey.load_from_bytes(bf.read())

    @staticmethod
    def load_from_file(filepath):
        w = Wallet(load_from_file=False, save_to_file=False)
        w.private_key = Wallet.load_priv_keys(filepath)
        return w

    @staticmethod
    def load_priv_keys(filepath):
        with open(filepath, "rb") as fkey:
            return load_pem_private_key(fkey.read(), password=None)


wallet = Wallet()
