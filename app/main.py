from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.clients.llm_client import FakeLlmClient, OpenAILlmClient
from app.core.config import get_settings
from app.core.exceptions import (
    AiRequestError,
    ReviewNotFoundError,
    ai_request_error_handler,
    review_not_found_handler,
)
from app.routers.review_router import router as review_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()

    if settings.fake_llm or settings.openai_api_key is None:
        app.state.llm_client = FakeLlmClient(settings)
    else:
        app.state.llm_client = OpenAILlmClient(settings)

    yield

    await app.state.llm_client.close()


app = FastAPI(title="Review Reply API", lifespan=lifespan)

app.include_router(review_router)

app.add_exception_handler(ReviewNotFoundError, review_not_found_handler)
app.add_exception_handler(AiRequestError, ai_request_error_handler)