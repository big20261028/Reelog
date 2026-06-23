from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Reelog API",
    description="루틴 인증 기반 숏폼 기록 서비스 API",
    version="0.1.0",
)

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

@app.get("/")
def root():
    return {"message" : "Reelog API is running"}

@app.get("/api/v1/health")
def health_check():
    return {
        "status": "ok",
        "service": "reelog-backend",
    }

@app.get("/api/v1/challenges")
def get_challenges():
    return [
        {
            "id": 1,
            "title": "아침 루틴 인증",
            "description": "기상, 물 마시기, 스트레칭을 인증하는 루틴",
        },
        {
            "id": 2,
            "title": "취준 루틴 인증",
            "description": "알고리즘, 프로젝트, CS 공부를 인증하는 루틴",
        }
    ]