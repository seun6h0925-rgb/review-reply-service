from dataclasses import dataclass


@dataclass
class Review:
    id: int  # 서버가 붙이는 리뷰 번호
    customer_name: str  # 손님 이름
    point: int  # 별점 (1~5)
    content: str  # 리뷰 내용
