launch:
	docker-compose up --remove-orphans

master:
	bash bbc.sh master

miner:
	bash bbc.sh miner

tx:
	bash bbc.sh tx MARTIAL 5 0.3

docker-image:
	docker build . -t babbagenode

# docker-run: # add master or miner as an argument
# 	docker run -it -v $$(pwd):/babbagecoin -p 5000:5000  babbagenode master
