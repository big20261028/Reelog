from pydantic import BaseModel, Field

class RoutineItemCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    sequence: int = Field(default=1, ge=1)


class RoutineItemResponse(BaseModel):
    id: int
    routine_id: int
    title: str
    description: str | None = None
    sequence: int

    model_config = {
        "from_attributes": True
    }

class RoutineCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)
    sequence: int = Field(default=1, ge=1)
    items: list[RoutineItemResponse] = Field(default_factory=list)


class RoutineUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)

class RoutineResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    items: list[RoutineItemResponse] = Field(default_factory=list)

    model_config = {
        "from_attributes" : True
    }