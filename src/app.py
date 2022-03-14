import sys
from miner.miner import run as miner_run
from master.routes import run as master_run

if __name__ == "__main__":
    command = sys.argv[1]
    if command == "master":
        master_run()
    elif command == "miner":
        miner_run()
