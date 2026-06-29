from datetime import datetime

from pydantic import BaseModel, Field

class RenderJobItemCreate(BaseModel):
    daily_routine_item_id: int
    proof_id: int

    sequence: int = Field(..., ge=1)

class RenderJobCreate(BaseModel):
    daily_routine_id: int
    
    items: list[RenderJobItemCreate] = Field(..., min_length=1)

class RenderJobItemResponse(BaseModel):
    id: int
    render_job_id: int
    daily_routine_item_id: int
    proof_id: int
    sequence: int

    model_config = {
        "from_attributes":True
    }


class RenderJobResponse(BaseModel):
    id: int
    daily_routine_id: int
    status: str
    output_media_asset_id: int | None = None
    error_message: str | None = None
    created_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None
    items: list[RenderJobItemResponse] = Field(default_factory=list)
    
    model_config = {
        "from_attributes":True
    }