from fastapi import Request
from fastapi.responses import JSONResponse


class ReviewNotFoundError(Exception):
    def __init__(self, review_id: int):
        self.review_id = review_id


class AiRequestError(Exception):
    def __init__(self, message: str):
        self.message = message


async def review_not_found_handler(request: Request, exc: ReviewNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"message": f"리뷰를 찾을 수 없습니다. (id={exc.review_id})"},
    )


async def ai_request_error_handler(request: Request, exc: AiRequestError):
    return JSONResponse(
        status_code=502,
        content={"message": exc.message},
    )
