FROM python:3.9-buster

# Setup poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="${PATH}:/root/.poetry/bin"
RUN poetry config virtualenvs.create false # system-wide package installation

WORKDIR /babbagecoin/

# copy only what `poetry install` needs, src code will be mapped as a volume
COPY pyproject.toml poetry.lock  ./

RUN poetry install --no-dev

# -u for unbuffered, so that python display each line of log asap
ENTRYPOINT ["python", "-u", "src/app.py"]
