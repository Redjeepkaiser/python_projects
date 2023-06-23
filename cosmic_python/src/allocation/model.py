from dataclasses import dataclass
from datetime import date
from typing import List, Optional, Set


@dataclass(unsafe_hash=True)
class OrderLine:
    order_id: str
    sku: str
    quantity: int


class Batch:
    def __init__(
        self, ref: str, sku: str, quantity: int, eta: Optional[date] = None
    ) -> None:
        self.ref: str = ref
        self.sku: str = sku
        self.eta: Optional[date] = eta
        self._purchased_quantity: int = quantity
        self._allocations: Set[OrderLine] = set()

    def __eq__(self, other) -> bool:
        if not isinstance(other, Batch):
            return False
        return other.ref == self.ref

    def __gt__(self, other) -> bool:
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def __hash__(self) -> int:
        return hash(self.ref)

    def allocate(self, order_line: OrderLine) -> None:
        if self.can_allocate(order_line):
            self._allocations.add(order_line)

    def can_allocate(self, order_line: OrderLine) -> bool:
        return (
            self.available_quantity >= order_line.quantity
            and self.sku == order_line.sku
        )

    def deallocate(self, order_line: OrderLine) -> None:
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


def allocate(
    order_line: OrderLine,
    batches: List[Batch],
) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(order_line))
        batch.allocate(order_line)
        return batch.ref
    except StopIteration:
        raise OutOfStock(f"Out of stock for sku {order_line.sku}")
