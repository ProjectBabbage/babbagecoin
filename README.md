# Babbagecoin

The project babbage proof of work blockchain.

Install docker and docker-compose.

## Launch

Run the node (master + miner)
`make` (= `docker-compose up`)

Run locally the master or miner
`make (master | miner)`

To make a transaction:
`make tx` -> this will send money to the best of us ;)

If you want to pass other arguments, use the bbc.sh script (chmod +x it first):
`./bbc.sh tx MARTIAL 10 0.5` (sending 10BBC with 0.5BBC fees to MARTIAL)