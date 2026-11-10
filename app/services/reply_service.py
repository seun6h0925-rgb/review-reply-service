from app.clients.llm_client import LlmClient
from app.schemas.review import ReplyResponse
from app.services.review_service import ReviewService

INSTRUCTIONS = (
    "너는 가게 사장님이다. "
    "손님 리뷰를 보고 별점에 맞춰 정중하고 따뜻한 답글을 두 세 문장으로 쓴다."
)


class ReplyService:
    def __init__(self, review_service: ReviewService, llm_client: LlmClient):
        self._review_service = review_service
        self._llm_client = llm_client

    async def create_reply(self, review_id: int) -> ReplyResponse:
        review = self._review_service.get_review(review_id)
        question = (
            f"손님: {review.customer_name}, "
            f"별점: {review.point}점, "
            f"리뷰: {review.content}"
        )
        text = await self._llm_client.ask_async(INSTRUCTIONS, question)
        return ReplyResponse(review_id=review_id, reply=text)
