from app.repositories.review_repository import ReviewRepository
from app.services.review_service import ReviewService

_review_repository = ReviewRepository()


def get_review_service() -> ReviewService:
    return ReviewService(_review_repository)