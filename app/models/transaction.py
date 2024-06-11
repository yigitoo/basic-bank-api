from datetime import datetime
from typing import Optional
from typing import Any
from sqlalchemy.sql.schema import Column
from sqlmodel import (
    Field,
    Integer,
    DateTime,
    Text,
    Float,
    Relationship
)
from sqlmodel.main import SQLModel


class Transaction(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    date : datetime = Field(DateTime)
    value: float = Field(Float)
    type: str = Field(Text)
    operator_name: str = Field(Text)
    account_id: int = Field(Integer, foreign_key='customer.id')
    account: Any = Relationship(back_populates='transfers')
