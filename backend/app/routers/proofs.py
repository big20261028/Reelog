from datetime import date, datetime
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.daily_routine import DailyRoutineItem
from app.models.proof import MediaAsset, Proof
from app.schemas.proof import ProofResponse

from app.routers.daily_routines import update_daily_routine_status

router = APIRouter(
    tags=["Proofs"]
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = BASE_DIR / "uploads" / "proofs"

ALLOWED_CONTENT_TYPES ={
    "image/jpeg",
    "image/png",
    "image/webp",
    "video/mp4",
    "video/quicktime",
}

# 한 item당 업로드 가능한 콘텐츠 개수
MAX_PROOFS_PER_ITEM = 5

@router.post(
    "/api/v1/daily-routine-items/{item_id}/proofs",
    response_model=ProofResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_proof(
    item_id: int,
    file: UploadFile = File(...),
    note: str | None = Form(default=None),
    db: Session = Depends(get_db)
):
    daily_routine_item = (
        db.query(DailyRoutineItem)
        .filter(DailyRoutineItem.id == item_id)
        .first()
    )

    if daily_routine_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="데일리 루틴 항목을 찾을 수 없습니다.",
        )
    
    current_proof_count = (
        db.query(Proof)
        .filter(Proof.daily_routine_item_id == item_id)
        .count()
    )

    if current_proof_count >= MAX_PROOFS_PER_ITEM:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"이 루틴 항목에는 인증 파일을 최대 {MAX_PROOFS_PER_ITEM}개까지만 등록할 수 있습니다.",
        )
    
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="지원하지 않는 파일 형식입니다.",
        )

    file_bytes = await file.read()

    if len(file_bytes) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="빈 파일은 업로드할 수 없습니다."
        )
    
    today_dir = UPLOAD_DIR / date.today().isoformat()
    today_dir.mkdir(parents=True, exist_ok=True)

    original_filename = file.filename or "upload"
    extension = Path(original_filename).suffix # 확장자 추출
    stored_filename = f"{uuid4().hex}{extension}" # 무작위 문자열과 확장자를 붙이기
    save_path = today_dir / stored_filename

    save_path.write_bytes(file_bytes)

    relative_path = save_path.relative_to(BASE_DIR)
    file_url = f"/uploads/proofs/{date.today().isoformat()}/{stored_filename}"

    media_asset = MediaAsset(
        original_filename=original_filename,
        stored_filename=stored_filename,
        file_path=str(relative_path),
        file_url=file_url,
        content_type=file.content_type,
        file_size=len(file_bytes),
    )

    proof = Proof(
        daily_routine_item_id=item_id,
        media_asset=media_asset,
        note=note,
    )

    daily_routine_item.is_completed = True
    
    if daily_routine_item.completed_at is None:
        daily_routine_item.completed_at = datetime.now()

    update_daily_routine_status(daily_routine_item.daily_routine)

    db.add(proof)
    db.commit()
    db.refresh(proof)

    return proof

@router.get(
    "/api/v1/daily-routine-items/{item_id}/proofs",
    response_model=list[ProofResponse],
)
def get_proofs_by_routine_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    daily_routine_item = (
        db.query(DailyRoutineItem)
        .filter(DailyRoutineItem.id == item_id)
        .first()
    )

    if daily_routine_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="데일리 루틴 항목을 찾을 수 없습니다.",
        )
    
    proofs = (
        db.query(Proof)
        .filter(Proof.daily_routine_item_id == item_id)
        # .order_by(Proof.created_at.desc())
        .all()
    )

    return proofs

@router.delete(
    "/api/v1/proofs/{proof_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_proof(
    proof_id: int,
    db: Session = Depends(get_db),
):
    proof = (
        db.query(Proof)
        .filter(Proof.id == proof_id)
        .first()
    )

    if proof is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="인증 기록을 찾을 수 없습니다."
        )
    
    daily_routine_item = proof.daily_routine_item

    media_asset = proof.media_asset
    file_path = BASE_DIR / media_asset.file_path

    db.delete(proof)
    db.delete(media_asset)
    db.flush()

    oldest_remaining_proof = (
        db.query(Proof)
        .filter(Proof.daily_routine_item_id == daily_routine_item.id)
        .order_by(Proof.created_at.asc(), Proof.id.asc())
        .first()
    )

    if oldest_remaining_proof is None:
        daily_routine_item.is_completed = False
        daily_routine_item.completed_at = None
    else:
        # 남은 proof중 가장 오래된 created_at 가져와서 등록하기
        daily_routine_item.is_completed = True
        daily_routine_item.completed_at = oldest_remaining_proof.created_at
    
    update_daily_routine_status(daily_routine_item.daily_routine)
    
    db.commit()

    if file_path.exists():
        file_path.unlink()

    return None