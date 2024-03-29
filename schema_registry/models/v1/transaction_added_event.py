# generated by datamodel-codegen:
#   filename:  transaction_added_event.json
#   timestamp: 2024-03-10T09:01:39+00:00

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class EventTitleTransactionAdded(Enum):
    TRANSACTION_ADDED = 'TRANSACTION.ADDED'


class TransactionTypes(Enum):
    INCOME = 'INCOME'
    EXPENSE = 'EXPENSE'
    PAYMENT = 'PAYMENT'


class TransactionAddedDataSchema(BaseModel):
    public_id: str = Field(..., title='Public Id')
    user_public_id: str = Field(..., title='User Public Id')
    debit: int = Field(..., title='Debit')
    credit: int = Field(..., title='Credit')
    type: TransactionTypes
    task_public_id: Optional[str] = Field(None, title='Task Public Id')


class AccountingProducer(Enum):
    BILLING_SERVICE = 'BILLING_SERVICE'


class TransactionAddedEventSchema(BaseModel):
    version: Optional[int] = Field(1, title='Version')
    produced_at: Optional[datetime] = Field(None, title='Produced At')
    title: Optional[EventTitleTransactionAdded] = 'TRANSACTION.ADDED'
    data: TransactionAddedDataSchema
    producer: Optional[AccountingProducer] = 'BILLING_SERVICE'
