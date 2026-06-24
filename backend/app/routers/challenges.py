from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.challenge import Challenge
from app.schemas.challenge import (
    ChallengeCreate,
    ChallengeUpdate,
    ChallengeResponse
)

router = APIRouter(
    prefix="/api/v1/challenges",
    tags=["Challenges"],
)

@router.get("", response_model=list[ChallengeResponse])
def get_challenges(db: Session = Depends(get_db)):
    challenges = db.query(Challenge).all()
    return challenges

@router.post(
    "",
    response_model=ChallengeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_challenge(
    payload: ChallengeCreate,
    db: Session = Depends(get_db)
    ):
    challenge = Challenge(
        title=payload.title,
        description=payload.description,
    )

    db.add(challenge)
    db.commit()
    db.refresh(challenge)

    return challenge

@router.get("/{challenge_id}", response_model=ChallengeResponse)
def get_challenge(
    challenge_id: int,
    db: Session = Depends(get_db)
    ):
    
    challenge = (
        db.query(Challenge)
        .filter(Challenge.id == challenge_id)
        .first()
    )
    
    if challenge is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='챌린지를 찾을 수 없습니다.'
        )
    
    return challenge

@router.patch("/{challenge_id}", response_model=ChallengeResponse)
def update_challenge(
    challenge_id: int, 
    payload: ChallengeUpdate,
    db: Session = Depends(get_db)
    ):

    challenge = (
        db.query(Challenge)
        .filter(Challenge.id == challenge_id)
        .first()
    )
   
    if challenge is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="챌린지를 찾을 수 없습니다.",
        )
    
    update_data = payload.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(challenge, key, value)

    db.commit()
    db.refresh(challenge)

    return challenge


@router.delete("/{challenge_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_challenge(
    challenge_id: int,
    db: Session = Depends(get_db)
    ):

    challenge = (
        db.query(Challenge).filter(Challenge.id == challenge_id).first()
    )

    if challenge is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="챌린지를 찾을 수 없습니다.",
        )

    db.delete(challenge)
    db.commit()

    return None

    