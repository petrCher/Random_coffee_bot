SHELL := /bin/bash

configure: venv
	source ./venv/bin/activate && pip install --force-reinstall -r requirements.txt -r requirements.dev.txt

venv:
	python3.12 -m venv venv

format:
	source ./venv/bin/activate && autoflake -r --in-place --remove-all-unused-imports ./src
	source ./venv/bin/activate && isort ./src
	source ./venv/bin/activate && black ./src

db:
	#docker

migrate:
	source ./venv/bin/activate && alembic upgrade head