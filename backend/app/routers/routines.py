from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.routine import Routine,RoutineItem
from app.schemas.routine import (
    RoutineCreate,
    RoutineItemCreate,
    RoutineItemResponse,
    RoutineResponse,
    RoutineUpdate,
)

router = APIRouter(
    prefix="/api/v1/routines",
    tags=["Routines"],
)

@router.get("", response_model=list[RoutineResponse])
def get_routines(db: Session = Depends(get_db)):
    routines = db.query(Routine).all()
    return routines

@router.post(
    "",
    response_model=RoutineResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_routine(
    payload: RoutineCreate,
    db: Session = Depends(get_db),
):
    routine = Routine(
        title=payload.title,
        description=payload.description,
    )

    for item_payload in payload.items:
        routine.items.append(
            RoutineItem(
                title=item_payload.title,
                description=item_payload.description,
                sequence=item_payload.sequence,
            )
        )
    
    db.add(routine)
    db.commit()
    db.refresh(routine)

    return routine


@router.get("/{routine_id}", response_model=RoutineResponse)
def get_routine(
    routine_id: int,
    db: Session = Depends(get_db)
):
    routine = (
        db.query(Routine)
        .filter(Routine.id == routine_id)
        .first()
    )

    if routine is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="루틴을 찾을 수 없습니다."
        )
    
    return routine

@router.patch("/{routine_id}", response_model=RoutineResponse)
def update_routine(
    routine_id: int,
    payload: RoutineUpdate,
    db: Session = Depends(get_db)
):
    routine = (
        db.query(Routine)
        .filter(Routine.id == routine_id)
        .first()
    )

    if routine is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="루틴을 찾을 수 없습니다.",
        )
    
    update_data = payload.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(routine, key, value)
     
    db.commit()
    db.refresh(routine)

    return routine


@router.delete("/{routine_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_routine(
    routine_id: int,
    db: Session = Depends(get_db)
):
    routine = (
        db.query(Routine)
        .filter(Routine.id == routine_id)
        .first()
    )

    if routine is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="루틴을 찾을 수 없습니다."
        )
    
    db.delete(routine)
    db.commit()

    return None

@router.post(
    "/{routine_id}/items",
    response_model=RoutineItemResponse,
    status_code=status.HTTP_201_CREATED
)
def create_routine_item(
    routine_id: int,
    payload: RoutineItemCreate,
    db: Session = Depends(get_db)
):
    routine = (
        db.query(Routine)
        .filter(Routine.id == routine_id)
        .first()
    )

    if routine is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="루틴을 찾을 수 없습니다."
        )
    
    item = RoutineItem(
        routine_id=routine_id,
        title=payload.title,
        description=payload.description,
        sequence=payload.sequence
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return item

@router.delete(
    "/{routine_id}/items/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_routine_item(
    routine_id: int,
    item_id: int,
    db: Session = Depends(get_db)
):
    item = (
        db.query(RoutineItem)
        .filter(
            RoutineItem.id == item_id,
            RoutineItem.routine_id == routine_id,
        )
        .first()
    )

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="루틴 항목을 찾을 수 없습니다."
        )
    
    db.delete(item)
    db.commit()

    return None