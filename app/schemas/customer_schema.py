from typing import TypeVar, Optional
from pydantic import BaseModel, Field

T = TypeVar('T')

class CustomerSchema(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None

    class Config:
        from_attributes = True


class RequestCustomer(BaseModel):
    parameter: CustomerSchema = Field(...)
