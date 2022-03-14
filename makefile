master:
	python src/app.py master

worker:
	python src/app.py worker

front:
	mkdir -p plot
	streamlit run src/frontend/app.py

docker-image:
	poetry export --without-hashes > generated-requirements.txt
	docker build . -t babbagenode

docker-run:
	docker run -it babbagenode


