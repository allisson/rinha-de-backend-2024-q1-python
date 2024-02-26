from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, model_serializer


class TransactionType(str, Enum):
    credit = "c"
    debit = "d"


class Transaction(BaseModel):
    amount: int = Field(alias="valor", gt=0)
    type: TransactionType = Field(alias="tipo")
    description: str = Field(alias="descricao", min_length=1, max_length=10)
    created_at: datetime = Field(alias="realizada_em", default_factory=datetime.utcnow)


class Client(BaseModel):
    id: int
    account_limit: int = Field(alias="limite")
    account_balance: int = Field(alias="saldo")
    transactions: list[Transaction] = Field(alias="ultimas_transacoes", default=[])

    @model_serializer
    def serialize_model(self):
        return {
            "saldo": {
                "total": self.account_balance,
                "data_extrato": datetime.utcnow().isoformat(),
                "limite": abs(self.account_limit),
            },
            "ultimas_transacoes": [
                {
                    "valor": t.amount,
                    "tipo": t.type.value,
                    "descricao": t.description,
                    "realizada_em": t.created_at,
                }
                for t in self.transactions
            ],
        }


class Error(BaseModel):
    code: int
    message: str
