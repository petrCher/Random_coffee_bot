SHELL := /bin/bash

configure: venv
	source ./venv/bin/activate && pip install -r requirements.txt

venv:
	python3.11 -m venv venv

format:
	#black isort

db:
	#docker

migrate:
	source ./venv/bin/activate && alembic upgrade head