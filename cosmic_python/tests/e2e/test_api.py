import pytest
# import requests

# @pytest.mark.usefixtures("restart_api")
# def test_api_returns_allocation(add_stock):
#     sku, other_sku = random_sku(), random_sku("other")
#     early_batch = random_batchref(1)
#     later_batch = random_batchref(2)
#     other_batch = random_batchref(3)
    
#     add_stock(
#         (later_batch, sku, 100, "2011-01-02"),
#         (later_batch, sku, 100, "2011-01-01"),
#         (later_batch, other_sku, 100, None),
#     )

#     data = {"order_id": random_order_id(), "sku": sku, "quantity": 3}
#     url = config.get_api_url()

#     r = requests.post(f"{url}/allocate", json=data)

#     assert r.status_code == 201
#     assert r.json()["batchref"] == early_batch
