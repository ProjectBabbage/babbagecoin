FROM python:3.9
WORKDIR /babbagecoin/
COPY . ./
RUN pip install -r generated-requirements.txt
ENTRYPOINT python src/app.py
