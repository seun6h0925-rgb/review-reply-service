from fastapi import Depends, Request

from app.clients.llm_client import LlmClient
from app.repositories.review_repository import ReviewRepository
from app.services.reply_service import ReplyService
from app.services.review_service import ReviewService

_review_repository = ReviewRepository()


def get_review_service() -> ReviewService:
    return ReviewService(_review_repository)


def get_llm_client(request: Request) -> LlmClient:
    return request.app.state.llm_client


def get_reply_service(
    review_service: ReviewService = Depends(get_review_service),
    llm_client: LlmClient = Depends(get_llm_client),
) -> ReplyService:
    return ReplyService(review_service, llm_client)