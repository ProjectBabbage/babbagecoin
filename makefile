launch:
	docker-compose --project-directory=. -f nodes/docker-compose.yml up --build

stop:
	docker-compose --project-directory=. -f nodes/docker-compose.yml down

master:
	bash bbc.sh master

miner:
	bash bbc.sh miner

tx:
	bash bbc.sh tx MARTIAL 5 0.3

docker-image:
	docker build . -t base_image_bbc

test-2:
	docker-compose --project-directory=. -f nodes/docker-compose-2.yml up --build

test-4:
	docker-compose --project-directory=. -f nodes/docker-compose-4.yml up --build