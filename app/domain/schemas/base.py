from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class BaseResponseList(BaseModel, Generic[T]):
    data: List[T]
    total: int
    page: int = 1
    limit: int = 25
    has_next: bool = False
    has_prev: bool = False