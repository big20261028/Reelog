from datetime import date, datetime

from pydantic import BaseModel

class DailyRoutineItemResponse(BaseModel):
    id: int
    daily_routine_id: int
    routine_item_id: int | None = None
    title: str
    description: str | None = None
    sequence: int
    is_completed: bool
    completed_at: datetime | None = None
    
    proof_count: int = 0

    model_config = {
        "from_attributes":True
    }
    
class DailyRoutineResponse(BaseModel):
    id: int
    routine_id: int
    target_date: date
    title: str
    description: str | None = None
    status: str
    items: list[DailyRoutineItemResponse] = []

    model_config = {
        "from_attributes": True
    }