from fastapi import FastAPI

from app.core.exceptions import ReviewNotFoundError, review_not_found_handler
from app.routers.review_router import router as review_router

app = FastAPI(title="Review Reply API")

app.include_router(review_router)

app.add_exception_handler(ReviewNotFoundError, review_not_found_handler)