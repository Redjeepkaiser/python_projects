import uuid
from typing import List, Optional, Tuple

import pytest
import requests

import config


def random_suffix() -> str:
    return uuid.uuid4().hex[:6]


def random_sku(name="") -> str:
    return f"sku-{name}-{random_suffix()}"


def random_batch_ref(name="") -> str:
    return f"batch-{name}-{random_suffix()}"


def random_order_id(name="") -> str:
    return f"order-{name}-{random_suffix()}"


def add_stock(batches: List[Tuple[str, str, int, Optional[str]]]):
    url = config.get_api_url()

    for ref, sku, quantity, eta in batches:
        r = requests.post(
            f"{url}/add_batch",
            json={"ref": ref, "sku": sku, "quantity": quantity, "eta": eta},
        )
        assert r.status_code == 201


@pytest.mark.usefixtures("restart_api")
def test_api_returns_allocation() -> None:
    pass
    sku, other_sku = random_sku(), random_sku("other")
    early_batch = random_batch_ref(1)
    later_batch = random_batch_ref(2)
    other_batch = random_batch_ref(3)

    add_stock(
        [
            (later_batch, sku, 100, "2011-01-02"),
            (early_batch, sku, 100, "2011-01-01"),
            (other_batch, other_sku, 100, None),
        ]
    )

    data = {"order_id": random_order_id(), "sku": sku, "quantity": 3}
    url = config.get_api_url()

    r = requests.post(f"{url}/allocate", json=data)

    assert r.status_code == 201
    assert r.json()["batchref"] == early_batch


@pytest.mark.usefixtures("restart_api")
def test_allocations_are_persisted() -> None:
    sku = random_sku()
    batch1, batch2 = random_batch_ref(1), random_batch_ref(2)
    order1, order2 = random_order_id(1), random_order_id(2)
    add_stock(
        [(batch1, sku, 10, "2011-01-01"), (batch2, sku, 10, "2011-01-02")]
    )
    line1 = {"orderid": order1, "sku": sku, "qty": 10}
    line2 = {"orderid": order2, "sku": sku, "qty": 10}
    url = config.get_api_url()

    # first order uses up all stock in batch 1
    r = requests.post(f"{url}/allocate", json=line1)
    assert r.status_code == 201
    assert r.json()["batchref"] == batch1

    # second order should go to batch 2
    r = requests.post(f"{url}/allocate", json=line2)
    assert r.status_code == 201
    assert r.json()["batchref"] == batch2
