SHELL := /bin/bash

configure: venv
	source ./venv/bin/activate && pip install -r requirements.txt -r requirements.dev.txt

venv:
	python3.11 -m venv venv

format:
	source ./venv/bin/activate && autoflake -r --in-place --remove-all-unused-imports ./src
	source ./venv/bin/activate && isort ./src
	source ./venv/bin/activate && black ./src

db:
	docker run -d -p 5432:5432 -e POSTGRES_HOST_AUTH_METHOD=trust --name db-random_coffee_bot postgres:15

migrate:
	source ./venv/bin/activate && alembic upgrade head

autogenerate:
	source ./venv/bin/activate && alembic revision --autogenerate -m "init"

run:
	source ./venv/bin/activate && python -m src