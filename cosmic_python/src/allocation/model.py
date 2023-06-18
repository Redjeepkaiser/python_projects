from datetime import date
from dataclasses import dataclass
from typing import List, Optional


@dataclass(unsafe_hash=True)
class OrderLine():
    order_id: str 
    sku: str 
    quantity: int 


class Batch():

    def __init__(self, ref: str, sku: str, quantity: int, eta: Optional[date] = None) -> None:
        self.ref = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = quantity
        self._allocations = set()

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.ref == self.ref

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def __hash__(self):
        return hash(self.ref)

    def allocate(self, order_line: OrderLine):
        if self.can_allocate(order_line):
            self._allocations.add(order_line)

    def can_allocate(self, order_line: OrderLine) -> bool:
        return self.available_quantity >= order_line.quantity and self.sku == order_line.sku

    def deallocate(self, order_line: OrderLine):
        if order_line in self._allocations:
            self._allocations.remove(order_line)

    @property
    def allocated_quantity(self) -> int:
        return sum(order_line.quantity for order_line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity


class OutOfStock(Exception):
    pass


def allocate(order_line: OrderLine, batches: List[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(order_line))
        batch.allocate(order_line)
        return batch.ref
    except StopIteration:
        raise OutOfStock(f"Out of stock for sku {order_line.sku}")

