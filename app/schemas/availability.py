from pydantic import BaseModel, model_validator
from uuid import UUID
from datetime import datetime

class AvailabilityCreate(BaseModel):
    start_time: datetime
    end_time: datetime

    @model_validator(mode="after")
    def validate_times(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        if self.start_time <= datetime.now(self.start_time.tzinfo):
            raise ValueError("start_time must be in the future")
        return self
    
class AvailabilityResponse(BaseModel):
    id: UUID
    user_id: UUID
    start_time: datetime
    end_time: datetime
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}