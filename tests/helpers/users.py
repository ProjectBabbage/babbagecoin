from tests.helpers.models import make_stx, make_block_with_reward
from babbagecoin.common.wallet import Wallet
from babbagecoin.common.models import PubKey, Block
from babbagecoin.common.balance import get_balance_of_address


class User:
    wallet: Wallet

    def __init__(self, user: str):
        self.wallet = Wallet.load_from_file(f"tests/fixtures/private_keys/{user}.txt")

    def pubkey(self) -> PubKey:
        return self.wallet.get_public_key()

    def address(self) -> str:
        return self.pubkey().hash()

    def balance(self) -> int:
        return get_balance_of_address(self.pubkey().hash())

    def new_transaction(self, receiver, amount=5, fees=0):
        return make_stx(self.wallet(), receiver.address(), amount, fees)

    def mine_new_block_after(self, block: Block, height=-1, stxs=[], next_blocks=[]) -> Block:
        if height == -1:
            height = block.height + 1
        return make_block_with_reward(block, self.address(), height, stxs, next_blocks)


user1 = User("USER1")
user2 = User("USER2")
