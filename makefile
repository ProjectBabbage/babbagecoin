master:
	PYTHONPATH=. python3 src/app.py worker

worker:
	PYTHONPATH=. python3 src/app.py worker
