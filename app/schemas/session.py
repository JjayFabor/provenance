from pydantic import BaseModel, model_validator
from uuid import UUID
from datetime import datetime, timezone, timedelta
from app.models.session import SessionStatus

class SessionCreate(BaseModel):
    skill_id: UUID
    start_time: datetime
    end_time: datetime
    note: str | None = None

    @model_validator(mode="after")
    def validate_times(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        if self.start_time <= datetime.now(timezone.utc):
            raise ValueError("start_time must be in the future")
        
        duration = self.end_time - self.start_time
        if duration < timedelta(minutes=30):
            raise ValueError("Session must be at least 30 minutes")
        if duration > timedelta(hours=2):
            raise ValueError("Session cannot exceed 2 hours")

        return self
    
class SessionResponse(BaseModel):
    id: UUID
    mentor_id: UUID
    learner_id: UUID
    skill_id: UUID
    start_time: datetime
    end_time: datetime
    status: SessionStatus
    note: str | None
    created_at: datetime

    model_config = {"from_attributes": True}

class SessionStatusUpdate(BaseModel):
    status: SessionStatus