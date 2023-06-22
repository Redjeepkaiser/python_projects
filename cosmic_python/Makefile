.PHONY: all down build up test test-unit test-integration test-e2e fmt-src fmt-tests fmt


all: install down build up test


install:
	@pip3 install -e .


run:
	@gunicorn -w 1 -b 127.0.0.1:5005 api:app


down:
	@docker-compose down --remove-orphans

build:
	@docker-compose build

up:
	@docker-compose up -d app


lint:
	@mypy .

test: build
	@docker-compose run --rm --no-deps --entrypoint="pytest" app /tests/unit /tests/integration /tests/e2e

test-unit: build
	@docker-compose run --rm --no-deps --entrypoint="pytest -v" app /tests/unit

test-integration: build
	@docker-compose run --rm --no-deps --entrypoint="pytest -v" app /tests/integration

test-e2e: build
	@docker-compose run --rm --no-deps --entrypoint="pytest -v" app /tests/e2e


fmt:
	@black .