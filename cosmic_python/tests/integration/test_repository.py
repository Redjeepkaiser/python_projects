from sqlalchemy import text

import allocation.domain.model as model
import allocation.adapters.repository as repository


def test_repository_can_save_a_batch(
    session,
):
    batch = model.Batch("batch-002", "SMALL-TABLE", 10)

    repo = repository.SqlAlchemyRepository(session)
    repo.add(batch)
    session.commit()

    rows = session.execute(
        text('SELECT ref, sku, _purchased_quantity, eta FROM "batches"')
    )
    assert list(rows) == [
        (
            "batch-002",
            "SMALL-TABLE",
            10,
            None,
        )
    ]


def insert_order_line(session):
    session.execute(
        text(
            "INSERT INTO order_lines (order_id, sku, quantity) "
            'values ("order1", "GENERIC-SOFA", 12)'
        )
    )
    [[orderline_id]] = session.execute(
        text(
            "SELECT id FROM order_lines WHERE order_id=:order_id AND sku=:sku"
        ),
        dict(
            order_id="order1",
            sku="GENERIC-SOFA",
        ),
    )
    return orderline_id


def insert_batch(session, batch_id):
    session.execute(
        text(
            "INSERT INTO batches (ref, sku, _purchased_quantity, eta)"
            ' VALUES (:batch_id, "GENERIC-SOFA", 100, null)'
        ),
        dict(batch_id=batch_id),
    )
    [[batch_id]] = session.execute(
        text(
            'SELECT id FROM batches WHERE ref=:batch_id AND sku="GENERIC-SOFA"'
        ),
        dict(batch_id=batch_id),
    )
    return batch_id


def insert_allocation(session, orderline_id, batch_id):
    session.execute(
        text(
            "INSERT INTO allocations (orderline_id, batch_id)"
            " VALUES (:orderline_id, :batch_id)"
        ),
        dict(
            orderline_id=orderline_id,
            batch_id=batch_id,
        ),
    )


def test_repository_can_retrieve_a_batch_with_allocations(
    session,
):
    orderline_id = insert_order_line(session)
    batch1_id = insert_batch(session, "batch1")
    insert_batch(session, "batch2")
    insert_allocation(session, orderline_id, batch1_id)

    repo = repository.SqlAlchemyRepository(session)
    retrieved = repo.get("batch1")

    expected = model.Batch(
        "batch1",
        "GENERIC-SOFA",
        100,
        eta=None,
    )
    assert retrieved == expected
    assert retrieved.sku == expected.sku
    assert retrieved._purchased_quantity == expected._purchased_quantity
    assert retrieved._allocations == {
        model.OrderLine("order1", "GENERIC-SOFA", 12),
    }
