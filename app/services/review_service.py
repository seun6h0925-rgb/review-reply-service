from app.core.exceptions import ReviewNotFoundError
from app.repositories.review_repository import ReviewRepository
from app.schemas.review import ReviewCreateRequest, ReviewResponse


class ReviewService:
    def __init__(self, repository: ReviewRepository):
        self._repository = repository

    def create_review(self, request: ReviewCreateRequest) -> ReviewResponse:
        review = self._repository.save(
            customer_name=request.customer_name,
            point=request.point,
            content=request.content,
        )
        return ReviewResponse(
            id=review.id,
            customer_name=review.customer_name,
            point=review.point,
            content=review.content,
        )

    def get_review(self, review_id: int) -> ReviewResponse:
        review = self._repository.find_by_id(review_id)
        if review is None:
            raise ReviewNotFoundError(review_id)
        return ReviewResponse(
            id=review.id,
            customer_name=review.customer_name,
            point=review.point,
            content=review.content,
        )
