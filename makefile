## Running bbc
launch:
	docker-compose --project-directory=. -f docker/docker-compose.yml up --build

stop:
	docker-compose --project-directory=. -f docker/docker-compose.yml down

master:
	bash bbc.sh master

miner:
	bash bbc.sh miner

docker-image:
	docker build . -t base_image_bbc

two-nodes:
	docker-compose --project-directory=. -f docker/docker-compose-2.yml up --build

four-nodes:
	docker-compose --project-directory=. -f docker/docker-compose-4.yml up --build

## Interacting with the node
tx:
	bash bbc.sh tx MARTIAL 5 0.3

balance:
	bash bbc.sh balance

## Dev jobs
lint:
	flake8

requirements:
	poetry export --without-hashes --dev -o requirements.manual.txt
# for the github actions to be lightweight and not to needs the installation of poetry

unittest:
	export TESTING=true
	python -m unittest discover --start-directory src

test:
	export TESTING=true
	pytest --cov=src src/tests --cov-report term:skip-covered --cov-fail-under 70