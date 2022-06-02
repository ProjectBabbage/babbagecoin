
from sentry_sdk import capture_message
from dataclasses import dataclass
from typing import Tuple
from common.block_service import delta_balance_block
from common.models import Block

@dataclass
class BalanceCache:
    balance: float
    last_block: Block

    def update_cache(self, balance, last_block):
        self.balance = balance
        self.last_block = last_block

    def __iter__(self):
        """So we can do stuff like `balance, block = BalanceCache()`"""
        return self.balance, self.last_block


class Database:
    def __init__(self):
        self.genesis = Block(prev_hash=None, height=0)
        self.block_tbl = { self.genesis.hash(): self.genesis }
        self.head = self.genesis
        self.balances = {}

    def __getattribute__(self, __name: str):
        super().__getattribute__(__name)

    def update_head(self, block):
        self.head = block

    def update_balance(self, address: str):
        bc = self.balances.get(address)
        if not bc:
            bc = BalanceCache(0, self.genesis)
            self.balances[address] = bc
        new_balance, new_last_block = self.compute_balance(address)
        bc.update_cache(new_balance, new_last_block)

    def compute_balance(self, address: str) -> Tuple[float, Block]:
        # balances[address] is supposed to exists at this point
        last_balance, last_block = self.balances[address]

        if not self.block_tbl[last_block.hash()]:
            # we recompute from genesis
            capture_message(f"The BalanceCache.last_block of hash {last_block.hash()} has be removed from block_tbl since the last cache computation for the address {address}")
            last_balance, last_block = 0, self.genesis

        while True:
            if last_block == self.head:
                break            
            if self.block_tbl[last_block.hash()].next_blocks:
                next_block = self.block_tbl[last_block.hash()].next_blocks[0]
                last_balance += delta_balance_block(address, next_block)
                last_block = next_block

        return last_balance, last_block

    def get_update_balance(self, address: str):
        self.update_balance(address)
        return self.balances.get(address)

    def update_block_table(self, block: Block):
        self.block_tbl[block.hash()] = block

