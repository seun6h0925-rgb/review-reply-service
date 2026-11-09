from fastapi import FastAPI

from app.routers.review_router import router as review_router

app = FastAPI(title="Review Reply API")

app.include_router(review_router)