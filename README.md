# University Helper Engine(UHE)

## UNDER CONSTRUCTION

## run dev server

`pip install e .`

`export FLASK_APP=run.py`

`export FLASK_DEBUG=1`

`flask run`

## run Celery

celery -A celery_worker.celery worker --beat --loglevel=info

## run Redis server