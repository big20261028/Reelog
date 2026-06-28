from datetime import datetime

from pydantic import BaseModel

class MediaAssetResponse(BaseModel):
    id: int
    original_filename: str
    stored_filename: str
    file_path: str
    file_url: str
    content_type: str
    file_size: int
    created_at: datetime

    model_config = {
        "from_attributes" : True #객체변환 auto
    }

class ProofResponse(BaseModel):
    id: int
    daily_routine_item_id: int
    media_asset_id: int
    note: str | None = None
    created_at: datetime
    media_asset: MediaAssetResponse

    model_config = {
        "from_attributes": True
    }
