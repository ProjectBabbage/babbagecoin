launch:
	docker-compose up

master:
	python src/app.py master

miner:
	python src/app.py miner

transaction:
	python src/app.py client MARTIAL 5 0.3

docker-image:
	docker build . -t babbagenode

# docker-run: # add master or miner as an argument
# 	docker run -it -v $$(pwd):/babbagecoin -p 5000:5000  babbagenode master
