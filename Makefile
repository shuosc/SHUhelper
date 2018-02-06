#!/bin/bash
.PHONY: clean install help test lint run dependencies docs

help:
	@echo "  clean      remove unwanted stuff"
	@echo "  test       run the testsuite"
	@echo "  lint       check the source for style errors"
	@echo "  run        run the development server with the development config"
	@echo "  docs       build the documentation"

SHELL=/bin/bash

dependencies:requirements.txt
	@echo "Installing dependencies..."
	@pip install -r requirements.txt 1>/dev/null

clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -rf {} +

install:
	@sudo pip3 install virtualenv
	@virtualenv env -p python3
	@source env/bin/activate
	@pip3 install -r requirements.txt

test:
	py.test

runweb:
	cd ./Web && yarn install
	cd ./Web && yarn dev
	cd ./Web && PORT=8081 yarn dev ios

installweb:
	cd ./Web && yarn install

buildweb:
	bash buildweb.sh

dev:
	source env/bin/activate && export FLASK_APP=run.py && export FLASK_DEBUG=1 && flask run

deploycelery:
	nohup celery -A celery_worker.celery worker --beat --loglevel=info & >celery.log

runcelery:
	celery -A celery_worker.celery worker --beat --loglevel=info
	
deploy:
	gunicorn -w 10 -k gevent  --reload -D -b 127.0.0.1:4001 --log-file gunicorn.log  --log-level debug --capture-output  wsgi:app

stopcelery:
	pkill -9 -f 'celery worker'

docs:
	$(MAKE) -C docs html

lint:check
	flake8

check:
	@type flake8 >/dev/null 2>&1 || echo "Flake8 is not installed. You can install it with 'pip install flake8'."