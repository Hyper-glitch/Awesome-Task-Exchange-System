# generated by datamodel-codegen:
#   filename:  task_cost_added_event.json
#   timestamp: 2024-03-10T08:59:39+00:00

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class EventTitleTaskCostAdded(Enum):
    TASK_COST_ADDED = 'TASK_COST.ADDED'


class TaskCostAddedDataSchema(BaseModel):
    public_id: str = Field(..., title='Public Id')
    task_public_id: str = Field(..., title='Task Public Id')
    debit_cost: int = Field(..., title='Debit Cost')
    credit_cost: int = Field(..., title='Credit Cost')


class AccountingProducer(Enum):
    BILLING_SERVICE = 'BILLING_SERVICE'


class TaskCostAddedEventSchema(BaseModel):
    version: Optional[int] = Field(1, title='Version')
    produced_at: Optional[datetime] = Field(None, title='Produced At')
    title: Optional[EventTitleTaskCostAdded] = 'TASK_COST.ADDED'
    data: TaskCostAddedDataSchema
    producer: Optional[AccountingProducer] = 'BILLING_SERVICE'