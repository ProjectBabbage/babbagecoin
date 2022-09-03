FROM python:3.9-bullseye

# Setup poetry
RUN pip install poetry
ENV PATH="${PATH}:/root/.poetry/bin"
# Unbuffered so that python displays each line of log ASAP
ENV PYTHONUNBUFFERED 1
RUN poetry config virtualenvs.create false # system-wide package installation

WORKDIR /babbagecoin/

# copy only what `poetry install` needs, src code will be mapped as a volume
COPY pyproject.toml poetry.lock  ./

RUN poetry install --only main

ENTRYPOINT ["python", "-m", "babbagecoin"]
