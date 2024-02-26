from psycopg.errors import CheckViolation, RaiseException
from psycopg.rows import class_row, dict_row
from psycopg_pool import ConnectionPool

from rinha_2024_q1.config import settings
from rinha_2024_q1.exceptions import ClientNotFound, InsufficientBalance
from rinha_2024_q1.model import Client

pool = ConnectionPool(
    settings.database_url,
    min_size=settings.database_pool_min_size,
    max_size=settings.database_pool_max_size,
    open=True,
)


def get_client(id):
    with pool.connection() as conn:
        with conn.cursor(row_factory=class_row(Client), binary=True) as cur:
            client = cur.execute(
                "SELECT * FROM clientes WHERE id = %(id)s", {"id": id}, prepare=True
            ).fetchone()
            if client is None:
                raise ClientNotFound
            return client


def add_transaction(id, transaction):
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row, binary=True) as cur:
            try:
                return cur.execute(
                    "SELECT add_transaction(%(id)s, %(transaction)s)",
                    {"id": id, "transaction": transaction.model_dump_json(by_alias=True)},
                    prepare=True,
                ).fetchone()
            except RaiseException:
                raise ClientNotFound
            except CheckViolation:
                raise InsufficientBalance
