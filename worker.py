import hashlib
import json
import time


class Transaction:
    def __init__(self, uuid, sender, receiver, amount):
        self.uuid = uuid
        self.sender = sender
        self.receiver = receiver
        self.amount = amount


class SignedTransaction:
    def __init__(self, transaction, signature):
        self.transaction = transaction
        self.signature = signature


class Block:
    def __str__(self):
        return json.dumps(self.__dict__)

    def __init__(self, prev_hash):
        self.prev_hash = prev_hash
        self.signed_transactions = []
        self.nounce = 0

    def hash(self) -> str:
        m = hashlib.sha256()
        s = str(self)
        b = s.encode("utf-8")
        m.update(b)
        m.digest()
        return m.hexdigest()


difficulty = 2000

bound = 2**256 / difficulty

b = Block("")
print(bound)

if __name__ == "__main__":
    t = time.time()
    count = 0
    while True:
        # print(f"{b.nounce}")
        h = int(b.hash(), 16)
        # print(h)
        if h <= bound:
            # print(b)
            count += 1
            if count >= 100:
                t2 = time.time()
                print(t2 - t)
                t = t2
                count = 0
        b.nounce += 1
