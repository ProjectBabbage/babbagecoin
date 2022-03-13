master:
	PYTHONPATH=. python3 src/app.py master

worker:
	PYTHONPATH=. python3 src/app.py worker

front:
	streamlit run src/frontend/app.py
