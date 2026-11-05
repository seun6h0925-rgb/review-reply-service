from app.schemas.base import CamelModel

from pydantic import Field

class Product(CamelModel):
    name: str
    stock: int = Field(ge=0, le=99)
    memo: str