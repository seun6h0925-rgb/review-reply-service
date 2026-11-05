class ReviewNotFoundError(Exception):
    def __init__(self,review_id: int):
        self.review_id = review_id