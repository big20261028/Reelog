from fastapi import APIRouter, HTTPException, status

from app.schemas.challenge import (
    ChallengeCreate,
    ChallengeUpdate,
    ChallengeResponse
)

router = APIRouter(
    prefix="/api/v1/challenges",
    tags=["Challenges"],
)

# DB를 붙이기 전까지 사용할 임시 메모리 저장소
challenges: list[dict] = [
    {
        "id": 1,
        "title": "아침 루틴 인증",
        "description": "기상, 물 마시기, 스트레칭을 인증하는 루틴",
    },
    {
        "id": 2,
        "title": "취준 루틴 인증",
        "description": "알고리즘, 프로젝트, CS 공부를 인증하는 루틴",
    },
]

next_challenge_id = 3


@router.get("", response_model=list[ChallengeResponse])
def get_challenges():
    return challenges

@router.post(
    "",
    response_model=ChallengeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_challenge(payload: ChallengeCreate):
    global next_challenge_id

    challenge = {
        "id" : next_challenge_id,
        "title": payload.title,
        "description": payload.description,
    }

    challenges.append(challenge)
    next_challenge_id += 1

    return challenge

@router.get("/{challenge_id}", response_model=ChallengeResponse)
def get_challenge(challenge_id: int):
    for challenge in challenges:
        if challenge["id"] == challenge_id:
            return challenge
        
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='챌린지를 찾을 수 없습니다.'
    )

@router.patch("/{challenge_id}", response_model=ChallengeResponse)
def update_challenge(challenge_id: int, payload: ChallengeUpdate):
    update_data = payload.model_dump(exclude_unset=True)

    for challenge in challenges:
        if challenge["id"] == challenge_id:
            challenge.update(update_data)
            return challenge

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="챌린지를 찾을 수 없습니다.",
    )


@router.delete("/{challenge_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_challenge(challenge_id: int):
    for index, challenge in enumerate(challenges):
        if challenge["id"] == challenge_id:
            challenges.pop(index) # 비효율
            return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="챌린지를 찾을 수 없습니다.",
    )