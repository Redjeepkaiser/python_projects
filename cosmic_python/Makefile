all: down build up test

down:
	docker-compose down --remove-orphans

build:
	docker-compose build

up:
	docker-compose up -d app

test: build
	docker-compose run --rm --no-deps --entrypoint="pytest" app /tests/unit /tests/integration /tests/e2e

test-unit: build
	docker-compose run --rm --no-deps --entrypoint="pytest -v" app /tests/unit

test-integration: build
	docker-compose run --rm --no-deps --entrypoint="pytest -v" app /tests/integration

test-e2e: build
	docker-compose run --rm --no-deps --entrypoint="pytest -v" app /tests/e2e
