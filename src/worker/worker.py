import time

from src.common.models import Block

def run():
    b = Block("")
    difficulty = 2000
    bound = 2 ** 256 / difficulty
    print(bound)

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
