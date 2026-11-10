from app.schemas.base import CamelModel

from pydantic import Field


class ReviewCreateRequest(CamelModel):
    customer_name: str
    point: int = Field(ge=1, le=5)
    content: str


class ReviewResponse(CamelModel):
    id: int
    customer_name: str
    point: int
    content: str


class ReplyResponse(CamelModel):
    review_id: int
    reply: str
