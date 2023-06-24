from typing import Dict, Tuple

from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from allocation import model, orm, repository

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)


@app.route("/", methods=["GET"])
def test() -> Tuple[Dict, int]:
    return {}, 200


@app.route("/allocate", methods=["POST"])
def allocate_endpoint() -> Tuple[Dict, int]:
    session = get_session()
    batches = repository.SqlAlchemyRepository(session).list()
    line = model.OrderLine(
        request.json["orderid"],
        request.json["sku"],
        request.json["qty"],
    )

    batchref = model.allocate(line, batches)

    return {"batchref": batchref}, 201
