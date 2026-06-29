from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pathlib import Path

from app.database import Base, engine
from app.models import challenge, routine, daily_routine, proof, render_job # 아무것도 안하는 것 같지만, 이게 있어야 SQLAlchemy가 모델 인식하고 테이블 생성.
from app.routers import challenges, routines, daily_routines, proofs, render_jobs

from fastapi.staticfiles import StaticFiles

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Reelog API",
    description="루틴 인증 기반 숏폼 기록 서비스 API",
    version="0.1.0",
)

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# React 개발 서버 주소
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(challenges.router)
app.include_router(routines.router)
app.include_router(daily_routines.router)
app.include_router(daily_routines.item_router)
app.include_router(proofs.router)
app.include_router(render_jobs.router)

@app.get("/")
def root():
    return {"message" : "Reelog API is running"}

@app.get("/api/v1/health")
def health_check():
    return {
        "status": "ok",
        "service": "reelog-backend",
    }

