import threading

from fastapi import APIRouter, Depends

from app.dependencies import get_reply_service, get_review_service
from app.schemas.review import ReplyResponse, ReviewCreateRequest, ReviewResponse
from app.services.reply_service import ReplyService
from app.services.review_service import ReviewService

router = APIRouter(prefix="/api/reviews", tags=["reviews"])


@router.post("", response_model=ReviewResponse, status_code=201)
def create_review(
    request: ReviewCreateRequest,
    service: ReviewService = Depends(get_review_service),
) -> ReviewResponse:
    return service.create_review(request)


@router.get("/{review_id}", response_model=ReviewResponse)
def get_review(
    review_id: int,
    service: ReviewService = Depends(get_review_service),
) -> ReviewResponse:
    return service.get_review(review_id)


@router.post("/{review_id}/reply", response_model=ReplyResponse)
async def create_reply(
    review_id: int,
    service: ReplyService = Depends(get_reply_service),
) -> ReplyResponse:
    print(f"[reply] 스레드: {threading.current_thread().name}")
    return await service.create_reply(review_id)