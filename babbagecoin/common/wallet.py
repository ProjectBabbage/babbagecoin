from pathlib import Path

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.exceptions import InvalidSignature

from babbagecoin.common.schemas import PrivateKeySchema, PubKeySchema
from babbagecoin.common.models import (
    MINING_REWARD_ADDRESS,
    PrivateKey,
    PubKey,
    Transaction,
    SignedTransaction,
)
from babbagecoin.common.exceptions import InvalidSignatureForTransaction
from babbagecoin.common.context import get_current_user


class Wallet:
    private_key: PrivateKey

    def __init__(self, load_from_file=True, save_to_file=True):
        self.private_key = PrivateKey(rsa.generate_private_key(public_exponent=65537, key_size=512))

        user_privk_filepath = f"private.key.{get_current_user()}.txt"
        if load_from_file and Path(user_privk_filepath).is_file():
            self.private_key = Wallet.load_priv_keys(user_privk_filepath)
            print(f"Found {user_privk_filepath}, using it.")
        if save_to_file and not Path(user_privk_filepath).is_file():
            self.save_files()
            print("Saving key files.")

    def public_key(self) -> PubKey:
        return self.private_key.derive_public_key()

    def save_files(self):
        """Create the private.key.<CURRENT_USER>.txt and public.key.<CURRENT_USER>.txt files."""
        user_private = f"private.key.{get_current_user()}.txt"
        user_public = f"public.key.{get_current_user()}.txt"
        with open(user_private, "w") as priv:
            priv.write(PrivateKeySchema.dumps(self.private_key))
        with open(user_public, "w") as pub:
            pub.write(PubKeySchema.dumps(self.public_key()))

    def sign(self, transaction: Transaction) -> str:
        return self.private_key.rsa_private_key.sign(
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
    def load_from_file(filepath) -> "Wallet":
        w = Wallet(load_from_file=False, save_to_file=False)
        w.private_key = Wallet.load_priv_keys(filepath)
        return w

    @staticmethod
    def load_priv_keys(filepath) -> PrivateKey:
        with open(filepath, "r") as fkey:
            return PrivateKeySchema.load(fkey.read())
            # return PrivateKey(load_pem_private_key(fkey.read(), password=None))


wallet = Wallet()
