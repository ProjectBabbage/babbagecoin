FROM python:3.9-buster

# Setup poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="${PATH}:/root/.poetry/bin"
RUN poetry config virtualenvs.create false # system-wide package installation

WORKDIR /babbagecoin/

COPY pyproject.toml poetry.lock  ./

RUN poetry install --no-dev

ENTRYPOINT ["python", "-u", "src/app.py"]

# # smaller, but first need a poetry export > requirements.txt
# FROM python:3.9
# WORKDIR /babbagecoin/
# COPY . ./
# RUN pip install -r requirements.txt
# ENTRYPOINT python src/app.py
