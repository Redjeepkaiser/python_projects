import pytest
from model import Batch, OrderLine, OutOfStock, allocate
from datetime import date, timedelta

today = date.today()
tomorrow = today + timedelta(days=1) 
later = today + timedelta(days=5) 


def test_prefers_current_stock_batches_to_shipments():
    in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
    shipment_batch = Batch("shipment-batch", "RETRO-CLOCK", 100, eta=tomorrow)
    order_line = OrderLine("order-ref", "RETRO-CLOCK", 20)

    allocate(order_line, [in_stock_batch, shipment_batch])

    assert in_stock_batch.available_quantity == 80
    assert shipment_batch.available_quantity == 100


def test_prefers_earlier_batches():
    earliest = Batch("earliest-batch", "RETRO-CLOCK", 100, eta=today)
    medium = Batch("medium-batch", "RETRO-CLOCK", 100, eta=tomorrow)
    latest = Batch("latest-batch", "RETRO-CLOCK", 100, eta=later)
    order_line = OrderLine("order-ref", "RETRO-CLOCK", 20)

    allocate(order_line, [earliest, medium, latest])

    assert earliest.available_quantity == 80
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100


def test_returns_allocated_batch_ref():
    in_stock_batch = Batch("in-stock-batch", "RETRO-CLOCK", 100, eta=None)
    shipment_batch = Batch("shipment-batch", "RETRO-CLOCK", 100, eta=tomorrow)
    order_line = OrderLine("order-ref", "RETRO-CLOCK", 20)

    allocation = allocate(order_line, [in_stock_batch, shipment_batch])

    assert allocation == in_stock_batch.ref 


def test_raises_out_of_stock_exception_if_cannot_allocate():
    shipment_batch = Batch("shipment-batch", "RETRO-CLOCK", 10)
    order_line = OrderLine("order-ref", "RETRO-CLOCK", 20)

    with pytest.raises(OutOfStock, match="RETRO-CLOCK"):
        allocate(order_line, [shipment_batch])



