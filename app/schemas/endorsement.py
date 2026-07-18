from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class EndorsementCreate(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: str | None = Field(default=None, max_length=500)


class EndorsementResponse(BaseModel):
    id: UUID
    skill_id: UUID
    endorser_id: UUID
    rating: int
    comment: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
