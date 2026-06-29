from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.daily_routine import DailyRoutine, DailyRoutineItem
from app.models.proof import Proof
from app.models.render_job import RenderJob, RenderJobItem
from app.schemas.render_job import RenderJobCreate, RenderJobResponse

RENDER_STATUS_PENDING = "PENDING"

router = APIRouter(
    prefix="/api/v1/render-jobs",
    tags=["Render Jobs"],
)

@router.post(
    "",
    response_model=RenderJobResponse,
    status_code=status.HTTP_201_CREATED
)
def create_render_job(
    payload: RenderJobCreate,
    db: Session = Depends(get_db),
):
    daily_routine = (
        db.query(DailyRoutine)
        .filter(DailyRoutine.id == payload.daily_routine_id)
        .first()
    )

    if daily_routine is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="데일리 루틴을 찾을 수 없습니다.",
        )
    
    selected_daily_routine_item_ids = set()
    selected_sequences = set()

    render_job = RenderJob(
        daily_routine_id=daily_routine.id,
        status=RENDER_STATUS_PENDING,
    )
    

    for item_payload in payload.items:
        if item_payload.daily_routine_item_id in selected_daily_routine_item_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="같은 루틴 항목을 중복해서 선택할 수 없습니다."
            )
        
        selected_daily_routine_item_ids.add(item_payload.daily_routine_item_id)

        if item_payload.sequence in selected_sequences:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="영상 순서는 중복될 수 없습니다."
            )
        
        selected_sequences.add(item_payload.sequence)

        daily_routine_item = (
            db.query(DailyRoutineItem)
            .filter(
                DailyRoutineItem.id == item_payload.daily_routine_item_id,
                DailyRoutineItem.daily_routine_id == daily_routine.id
            )
            .first()
        )

        if daily_routine_item is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="해당 데일리 루틴에 속하지 않는 루틴 항목입니다."
            )
        
        proof = (
            db.query(Proof)
            .filter(
                Proof.id == item_payload.proof_id,
                Proof.daily_routine_item_id == daily_routine_item.id
            )
            .first()
        )

        if proof is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="해당 루틴 항목에 속하지 않는 인증 파일입니다.",
            )
        
        render_job.items.append(
            RenderJobItem(
                daily_routine_item_id=item_payload.daily_routine_item_id,
                proof_id=item_payload.proof_id,
                sequence=item_payload.sequence,
            )
        )
    
    db.add(render_job)
    db.commit()
    db.refresh(render_job)

    return render_job

@router.get("", response_model=list[RenderJobResponse])
def get_render_jobs(db: Session = Depends(get_db)):
    render_jobs = (
        db.query(RenderJob)
        .order_by(RenderJob.id.desc())
        .all()
    )
        
    return render_jobs

@router.get("/{render_job_id}", response_model=RenderJobResponse)
def get_render_job(
    render_job_id: int,
    db: Session = Depends(get_db)
):
    render_job = (
        db.query(RenderJob)
        .filter(RenderJob.id == render_job_id)
        .first()
    )

    if render_job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="영상 제작 요청을 찾을 수 없습니다."
        )
    
    return render_job