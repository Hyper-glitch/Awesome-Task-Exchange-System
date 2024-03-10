# generated by datamodel-codegen:
#   filename:  user_created_event.json
#   timestamp: 2024-03-10T09:02:09+00:00

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class EventTitleUserCreated(Enum):
    USER_CREATED = 'USER.CREATED'


class UserRoles(Enum):
    EMPLOYEE = 'EMPLOYEE'
    ADMIN = 'ADMIN'
    MANAGER = 'MANAGER'


class UserDataSchema(BaseModel):
    public_id: str = Field(..., title='Public Id')
    username: str = Field(..., title='Username')
    email: str = Field(..., title='Email')
    role: UserRoles


class UserProducer(Enum):
    AUTH_SERVICE = 'AUTH_SERVICE'


class UserCreatedEventSchema(BaseModel):
    version: Optional[int] = Field(1, title='Version')
    produced_at: Optional[datetime] = Field(None, title='Produced At')
    title: Optional[EventTitleUserCreated] = 'USER.CREATED'
    data: UserDataSchema
    producer: Optional[UserProducer] = 'AUTH_SERVICE'
