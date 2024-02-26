import fastwsgi

from rinha_2024_q1.config import settings
from rinha_2024_q1.database import add_transaction, get_client
from rinha_2024_q1.handler import Handler
from rinha_2024_q1.model import Transaction, TransactionType


def warnup():
    for x in range(50):
        get_client(9999)

    for x in range(50):
        add_transaction(
            9999, Transaction(valor=100, tipo=TransactionType.credit.value, descricao="descricao")
        )


def app(environ, start_response):
    return Handler(environ, start_response).run()


if __name__ == "__main__":
    warnup()
    fastwsgi.run(wsgi_app=app, host=settings.server_host, port=settings.server_port)
