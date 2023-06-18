from allocation.model import Batch, OrderLine
from datetime import date


def make_batch_and_order_line(sku: str, batch_quantity: int, order_line_quantity: int):
    return (
        Batch("batch-002", sku, batch_quantity, date.today()),
        OrderLine("order-ref", sku, order_line_quantity),
    )

def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch, order_line = make_batch_and_order_line("SMALL-TABLE", 20, 2)
    batch.allocate(order_line)
    assert batch.available_quantity == 18


def test_can_allocate_if_available_greater_than_required():
    batch, order_line = make_batch_and_order_line("SMALL-TABLE", 20, 2)
    assert batch.can_allocate(order_line)


def test_can_allocate_if_available_equal_to_required():
    batch, order_line = make_batch_and_order_line("SMALL-TABLE", 5, 5)
    assert batch.can_allocate(order_line) is True


def test_cannot_allocate_if_available_smaller_than_required():
    batch, order_line = make_batch_and_order_line("SMALL-TABLE", 2, 20)
    assert batch.can_allocate(order_line) is False


def test_cannot_allocate_if_skus_do_not_match():
    batch = Batch("batch-002", "SMALL-TABLE", 10, date.today())
    order_line = OrderLine("order-ref", "BIG-TABLE", 2)
    assert batch.can_allocate(order_line) is False


def test_deallocate_from_a_batch_increases_the_available_quantity():
    batch, order_line = make_batch_and_order_line("SMALL-TABLE", 20, 2)
    batch.allocate(order_line)
    assert batch.available_quantity == 18
    batch.deallocate(order_line)
    assert batch.available_quantity == 20


def test_can_only_deallocate_allocated_lines():
    batch, order_line = make_batch_and_order_line("SMALL-TABLE", 20, 2)
    batch.deallocate(order_line)
    assert batch.available_quantity == 20


def test_allocation_is_idempotent():
    batch, line = make_batch_and_order_line("ANGULAR-DESK", 20, 2)
    batch.allocate(line)
    batch.allocate(line)
    assert batch.available_quantity == 18

