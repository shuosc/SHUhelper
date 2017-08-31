.PHONY: clean install help test lint run dependencies docs

help:
	@echo "  clean      remove unwanted stuff"
	@echo "  test       run the testsuite"
	@echo "  lint       check the source for style errors"
	@echo "  run        run the development server with the development config"
	@echo "  docs       build the documentation"


dependencies:requirements.txt
	@echo "Installing dependencies..."
	@pip install -r requirements.txt 1>/dev/null

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

test:
	py.test

runweb:
	cd ./UHE-frontend-Vue && yarn dev

buildweb:
	cd ./UHE-frontend-Vue && yarn build

run:
	# celery -A celery_worker.celery worker --loglevel=info & >celery.log
	export FLASK_APP=run.py && export FLASK_DEBUG=1 && flask run

deploycelery:
	celery -A celery_worker.celery worker --beat --loglevel=info & >celery.log

runcelery:
	celery -A celery_worker.celery worker --beat --loglevel=info


stopcelery:
	pkill -9 -f 'celery worker'

docs:
	$(MAKE) -C docs html

lint:check
	flake8

check:
	@type flake8 >/dev/null 2>&1 || echo "Flake8 is not installed. You can install it with 'pip install flake8'."