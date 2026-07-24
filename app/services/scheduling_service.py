from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from datetime import datetime
from app.models.availability import Availability
from app.models.session import BookingSession, SessionStatus


def is_within_availability(
    db: Session,
    mentor_id,
    start_time: datetime,
    end_time: datetime
) -> bool:
    availability = db.execute(
        select(Availability).where(
            and_(
                Availability.user_id == mentor_id,
                Availability.start_time <= start_time,
                Availability.end_time >= end_time,
                Availability.is_active == True
            )
        )
    ).scalars().first()

    return availability is not None

def has_scheduling_conflict(
    db: Session,
    mentor_id,
    start_time: datetime,
    end_time: datetime
) -> bool:
    conflict = db.execute(
        select(BookingSession).where(
            and_(
                BookingSession.mentor_id == mentor_id,
                BookingSession.status.not_in([
                    SessionStatus.cancelled,
                    SessionStatus.completed
                ]),
                BookingSession.start_time < end_time,
                BookingSession.end_time > start_time
            )
        )
    ).scalars().first()

    return conflict is not None