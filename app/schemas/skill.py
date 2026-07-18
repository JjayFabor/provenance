from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class SkillCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)


class SkillResponse(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    description: str | None
    credibility_score: float
    created_at: datetime

    model_config = {"from_attributes": True}