from app.repositories.review_repository import ReviewRepository


class ReviewService:
    def __init__(self, repository: ReviewRepository):
        self._repository = repository


    def create_review(self, request:ReviewCreateRequest) -> ReviewResponse:
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