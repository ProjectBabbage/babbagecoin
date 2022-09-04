# Babbagecoin

### An understandable proof of work blockchain.

**Visit our [web page](https://projectbabbage.github.io/babbagecoin/) for a nice general overview of the project !**

## Quickly run a node !


```bash
pip install --user babbagecoin
```

```bash
python -m babbagecoin master
# then in another terminal:
python -m babbagecoin miner
```

# For development

## Requirements

Install `docker` and `docker-compose`, `python3` (>=3.9) and `poetry`.

Run `poetry install` then `poetry shell`

## Launch

Run the node (master + miner):

`make`

Stop the node properly:

`make stop` --> to stop all containers if you didn't stopped them properly (if you did two Ctrl+C in a row)

Or you can run separately the master or miner:

`make (master | miner)`

There are also VSCode actions for debugging each one of them (even the tests, run in terminal with `make test`)

## Interact with the blockchain

!! Important

Configure your blockchain by creating a `.env` file on the same model as what's in `.env.example`.

The wallet will generate a private key for you, save it to private.key.<CURRENT_USER>, and reuse it afterward. A public key is derived from this private key. The hash of the public key is your address, for example e93417c7 (the first 8 characters).
The wallet is managing only one private key at the time.

### Transactions

Use the `bbc.sh` script (`chmod +x` it first):

`./bbc.sh tx MARTIAL 10 0.3` --> sending 10BBC with 0.5BBC fees to MARTIAL

_`make tx` is a shortcut for the above command_

### Balance

`./bbc.sh balance` to get your wallet balance

_`make balance` is a shortcut for the above command_

