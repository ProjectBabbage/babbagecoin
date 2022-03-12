import sys
from worker.worker import run as worker_run
from master.routes import run as master_run

if __name__ == "__main__":
    command = sys.argv[1]
    print(sys.argv[1])
    if command == "master":
        master_run()
    elif command == "worker":
        worker_run()
