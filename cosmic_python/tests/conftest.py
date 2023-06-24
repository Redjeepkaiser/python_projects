import time
from pathlib import Path

import pytest
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

import config
from allocation.orm import metadata, start_mappers


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    print("I AM CALLED")
    start_mappers()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()
    print("I AM CLEANED UP")


def wait_for_webapp_to_come_up():
    deadline = time.time() + 10
    url = config.get_api_url()

    print(url)

    while time.time() < deadline:
        try:
            return requests.get(url)
        except ConnectionError:
            time.sleep(0.5)
    pytest.fail("API never came up")


@pytest.fixture
def restart_api():
    (Path(__file__).parent / "../src/api/flask_app.py").touch()
    time.sleep(0.5)
    wait_for_webapp_to_come_up()
