# 리뷰와 사장님 답글 API

손님이 남긴 리뷰를 저장하고, 리뷰 내용과 별점을 바탕으로 OpenAI가 사장님 답글을 대신 써 주는 FastAPI 서버입니다.

## 기능

| 메서드 | 주소 | 설명 | 성공 | 실패 |
|---|---|---|---|---|
| POST | `/api/reviews` | 리뷰 등록 | 201 | 422 (별점이 1~5가 아님 등) |
| GET | `/api/reviews/{review_id}` | 리뷰 조회 | 200 | 404 (없는 리뷰) |
| POST | `/api/reviews/{review_id}/reply` | AI 사장님 답글 생성 | 200 | 404 (없는 리뷰), 502 (OpenAI 호출 실패) |

- 요청과 응답 JSON의 키는 camelCase입니다. (`customerName`, `reviewId`)
- 리뷰는 서버 메모리(딕셔너리)에 저장하므로 서버를 다시 켜면 사라집니다.
- 등록과 조회는 `def`, 답글 생성은 `async def`이며 OpenAI를 `await`로 호출합니다.

### 요청과 응답 예시

```json
// POST /api/reviews
{ "customerName": "김철수", "point": 5, "content": "음식이 정말 맛있었어요" }

// 201
{ "id": 1, "customerName": "김철수", "point": 5, "content": "음식이 정말 맛있었어요" }
```

```json
// POST /api/reviews/1/reply  → 200
{ "reviewId": 1, "reply": "김철수님, 맛있게 드셔주셔서 정말 감사합니다! ..." }

// 키가 틀리는 등 OpenAI 호출이 실패하면 502
{ "message": "OpenAI API 키가 올바르지 않습니다. OPENAI_API_KEY를 확인하세요." }
```

## 실행 방법

필요한 것: Python 3.14 이상, [uv](https://docs.astral.sh/uv/)

```bash
uv sync
uv run fastapi dev
```

서버가 켜지면 http://127.0.0.1:8000/docs 에서 API를 시험할 수 있습니다.

### OpenAI 키 설정

환경 변수 `OPENAI_API_KEY`를 등록하거나, 프로젝트 폴더에 `.env` 파일을 만들어 아래처럼 적습니다. (`.env`는 Git에 올라가지 않습니다.)

```
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-6-luna
```

키가 없거나 `FAKE_LLM=true`이면 OpenAI를 호출하지 않고 가짜 응답을 돌려주는 클라이언트를 사용합니다.

## 폴더 구조

```
app/
├─ main.py                      앱 생성, 라우터·예외 처리기 등록, lifespan(LLM 클라이언트 생성)
├─ dependencies.py              의존성 함수 (저장소 1개 공유, 서비스 생성)
├─ core/
│  ├─ config.py                 설정 읽기 (환경 변수, .env)
│  └─ exceptions.py             사용자 정의 예외와 처리기 (404, 502)
├─ domain/review.py             리뷰 엔티티
├─ repositories/review_repository.py   리뷰 저장소 (딕셔너리)
├─ schemas/                     요청·응답 DTO (camelCase)
├─ clients/llm_client.py        OpenAI 호출 (동기·비동기·가짜 클라이언트)
├─ services/
│  ├─ review_service.py         리뷰 등록·조회
│  └─ reply_service.py          리뷰를 읽어 AI 답글 생성
└─ routers/review_router.py     API 주소
```

## 확인한 내용

- 별점 6으로 등록하면 422가 응답됩니다.
- 없는 리뷰 번호를 조회하면 404가 응답됩니다.
- 답글 생성 핸들러는 `MainThread`에서 실행됩니다. (서버 로그에 `[reply] 스레드: MainThread` 출력)
- 잘못된 API 키로 답글을 요청하면 502가 응답됩니다.

## 개발 과정

기능마다 브랜치를 나누어 작업하고 `--no-ff`로 병합했습니다. 커밋 메시지는 `type(scope): 내용` 형식입니다.
