from app.domain.review import Review


class ReviewRepository:
    def __init__(self) -> None:
        self._reviews: dict[int, Review] = {}
        self._next_id = 1

    def save(self, customer_name: str, point: int, content: str) -> Review:
        review = Review(id=self._next_id, customer_name=customer_name, point=point, content=content)
        self._reviews[review.id] = review
        self._next_id += 1
        return review

    def find_by_id(self, review_id: int) -> Review | None:
        return self._reviews.get(review_id)