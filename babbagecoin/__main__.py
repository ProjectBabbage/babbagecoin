import sys
from babbagecoin.miner.miner import run as miner_run
from babbagecoin.master.routes import app as master_app
from babbagecoin.client.client import send_transaction, check_balance


if __name__ == "__main__":
    command = sys.argv[1]
    if command == "master":
        master_app.run(debug=True, host="0.0.0.0")
    elif command == "miner":
        miner_run()
    elif command == "tx":
        send_transaction(*sys.argv[2:])
    elif command == "balance":
        check_balance()
