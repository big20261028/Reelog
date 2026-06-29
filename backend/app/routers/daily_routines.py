from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.daily_routine import DailyRoutine, DailyRoutineItem
from app.models.routine import Routine
from app.models.proof import Proof
from app.schemas.daily_routine import (
    DailyRoutineItemResponse,
    DailyRoutineResponse,
)

STATUS_PENDING = "PENDING"
STATUS_IN_PROGRESS = "IN_PROGRESS"
STATUS_COMPLETED = "COMPLETED"

router = APIRouter(
    prefix="/api/v1/daily-routines",
    tags=["Daily Routines"],
)

item_router = APIRouter(
    prefix="/api/v1/daily-routine-items",
    tags=["Daily Routine Items"],
)

def update_daily_routine_status(daily_routines: DailyRoutine):
    items = daily_routines.items
    
    if len(items) == 0:
        daily_routines.status = STATUS_PENDING
        return
    
    completed_count = sum(1 for item in items if item.is_completed)
    
    if completed_count == 0:
        daily_routines.status = STATUS_PENDING
    elif completed_count == len(items):
        daily_routines.status = STATUS_COMPLETED
    else:
        daily_routines.status = STATUS_IN_PROGRESS
        
        
@router.post(
    "/from-routine/{routine_id}",
    response_model=DailyRoutineResponse,
    status_code=status.HTTP_201_CREATED
)
def create_daily_routine_from_routine(
    routine_id: int,
    db: Session = Depends(get_db)
):
    today = date.today()
    
    routine = (
        db.query(Routine)
        .filter(
            Routine.id == routine_id,
        )
        .first()
    )
    
    if routine is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="루틴 템플릿을 찾을 수 없습니다.",
        )
        
    existing_daily_routine = (
        db.query(DailyRoutine)
        .filter(
            DailyRoutine.routine_id == routine_id,
            DailyRoutine.target_date == today,
        )
        .first()
    )
    
    if existing_daily_routine is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 오늘 생성된 데일리 루틴이 있습니다."
        )

    daily_routine = DailyRoutine(
        routine_id=routine.id,
        target_date=today,
        title=routine.title,
        description=routine.description,
        status=STATUS_PENDING
    )
    
    for routine_item in routine.items:
        daily_routine.items.append(
            DailyRoutineItem(
                routine_item_id=routine_item.id,
                title=routine_item.title,
                description=routine_item.description,
                sequence=routine_item.sequence,
                is_completed=False,
            )
        )
    
    db.add(daily_routine)
    db.commit()
    db.refresh(daily_routine)
    
    return daily_routine

@router.get("/today", response_model=list[DailyRoutineResponse])
def get_today_daily_routines(db: Session = Depends(get_db)):
    today = date.today()
    
    daily_routines = (
        db.query(DailyRoutine)
        .filter(DailyRoutine.target_date == today)
        .order_by(DailyRoutine.id.desc())
        .all()
    )
    
    return daily_routines

@router.get("/{daily_routine_id}", response_model=DailyRoutineResponse)
def get_daily_routine(
    daily_routine_id: int,
    db: Session = Depends(get_db)
):
    daily_routine = (
        db.query(DailyRoutine)
        .filter(DailyRoutine.id == daily_routine_id)
        .first()
    )
    
    if daily_routine is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="데일리 루틴을 찾을 수 없습니다."
        )
    
    return daily_routine

@item_router.patch(
    "/{item_id}/complete",
    response_model=DailyRoutineItemResponse
)
def complete_daily_routine_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    item = (
        db.query(DailyRoutineItem)
        .filter(DailyRoutineItem.id == item_id)
        .first()
    )
    
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="데일리 루틴 항목을 찾을 수 없습니다."
        )

    item.is_completed = True
    item.completed_at = datetime.now()
    
    update_daily_routine_status(item.daily_routine) # daily_routine 필드 사용
    
    db.commit()
    db.refresh(item)
    
    return item
    
@item_router.patch(
    "/{item_id}/cancel",
    response_model=DailyRoutineItemResponse,
)
def cancel_daily_routine_item(
    item_id: int,
    db: Session = Depends(get_db),
):
    item = (
        db.query(DailyRoutineItem)
        .filter(DailyRoutineItem.id == item_id)
        .first()
    )

    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="데일리 루틴 항목을 찾을 수 없습니다.",
        )

    existing_proof_count = (
        db.query(Proof)
        .filter(Proof.daily_routine_item_id == item.id)
        .count()
    )

    if existing_proof_count > 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="인증 파일이 있는 항목은 완료 취소할 수 없습니다. 인증 파일을 먼저 삭제하세요."
        ) 

    item.is_completed = False
    item.completed_at = None

    update_daily_routine_status(item.daily_routine)

    db.commit()
    db.refresh(item)

    return item
    

        
        