## RUNNING BBC IN CONTAINERS
compose-up:
	docker-compose --project-directory=. -f docker/docker-compose.yml up --build

compose-stop:
	docker-compose --project-directory=. -f docker/docker-compose.yml down

compose-two-miners:
	docker-compose --project-directory=. -f docker/docker-compose-2.yml up --build

compose-four-miners:
	docker-compose --project-directory=. -f docker/docker-compose-4.yml up --build

# OR DIRECTLY ON YOUR MACHINE
master:
	bash bbc.sh master

miner:
	bash bbc.sh miner


# BUILD THE BASE IMAGE
docker-image:
	docker build . -t base_image_bbc


## Interacting with the node
tx:
	bash bbc.sh tx MARTIAL 5 0.3

balance:
	bash bbc.sh balance


# DEV JOBS
install:
	poetry install && poetry shell

lint:
	flake8

# not used much, prefer 'test' (using the pytest framework) command over this one
unittest:
	export TESTING=true
	python -m unittest discover --start-directory tests -v

# using pytest-forked to run each test in isolation in a forked subprocess (--forked)
# using pytest-xdist to run tests in parallel in four processes (-n 4)
test:
	export TESTING=true
	pytest -n 4 --forked --cov=babbagecoin tests --cov-report term:skip-covered --cov-fail-under 50


package:
	poetry build

package-publish:
	poetry publish
