from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, Field

T = TypeVar('T')

class APIRequest(BaseModel, Generic[T]):
    parameter: Optional[T] = Field(...)

class APIResponse(BaseModel, Generic[T]):
    code: int
    status: str
    message: str
    result: Optional[T]
