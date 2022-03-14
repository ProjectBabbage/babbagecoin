master:
	python src/app.py master

worker:
	python src/app.py worker

front:
	mkdir -p plot
	streamlit run src/frontend/app.py

docker:
	poetry export > requirements.txt
	docker build . -t babbagecoin
