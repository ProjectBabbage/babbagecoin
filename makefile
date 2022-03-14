master:
	python src/app.py master

miner:
	python src/app.py miner

front:
	mkdir -p plot
	streamlit run src/frontend/app.py

launch:
	docker-compose up
	
# docker-image:
# 	docker build . -t babbagenode

# docker-run: # add master or miner as an argument
# 	docker run -it -v $$(pwd):/babbagecoin -p 5000:5000  babbagenode master


