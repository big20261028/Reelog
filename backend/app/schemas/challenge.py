from pydantic import BaseModel, Field

class ChallengeCreate(BaseModel):
    # ... 의 의미 : 기본값이 없음. 반드시 요청에서 받아야 함.
    # 필수 필드 표시로 쓰임
    title: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)

class ChallengeUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)

class ChallengeResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    