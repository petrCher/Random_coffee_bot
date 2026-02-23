SHELL := /bin/bash

configure: venv
	source ./venv/bin/activate && pip install --force-reinstall -r requirements.txt

venv:
	python3.12 -m venv venv

format:
	#black isort

db:
	#docker

migrate:
	source ./venv/bin/activate && alembic upgrade head