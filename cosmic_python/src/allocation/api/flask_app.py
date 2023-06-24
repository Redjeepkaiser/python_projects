from datetime import datetime
from typing import Dict, Tuple

from flask import Flask, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import allocation.config as config
from allocation.adapters import orm, repository
from allocation.domain import model

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
app = Flask(__name__)


@app.route("/", methods=["GET"])
def add_batch() -> Tuple[Dict, int]:
    return {}, 200


# @app.route("/add_batch", methods=["POST"])
# def add_batch() -> Tuple[Dict, int]:
#     session = get_session()
#     repo = repository.SqlAlchemyRepository(session)
#     eta = request.json["eta"]

#     if eta is not None:
#         eta = datetime.fromisoformat(eta).date()

#     services.add_batch(
#         request.json["ref"],
#         request.json["sku"],
#         request.json["qty"],
#         eta,
#         repo,
#         session,
#     )

#     return "OK", 201


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
