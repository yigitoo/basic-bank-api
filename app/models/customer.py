from typing import Optional
from sqlmodel import (
    Column,
    Field,
    Integer,
    Text,
    Relationship
)
from sqlmodel.main import SQLModel

from app.models.transaction import Transaction
from app.database.config import Base

class Customer(SQLModel, Base):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(Text)
    transfers: list["Transaction"] = Relationship(back_populates='account')
