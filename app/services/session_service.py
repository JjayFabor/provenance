from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.session import BookingSession, SessionStatus
from app.models.skill import Skill
from app.models.user import User
from app.schemas.session import SessionCreate
from app.services.scheduling_service import is_within_availability, has_scheduling_conflict

VALID_TRANSITIONS = {
    SessionStatus.pending: [SessionStatus.confirmed, SessionStatus.cancelled],
    SessionStatus.confirmed: [SessionStatus.in_progress, SessionStatus.cancelled],
    SessionStatus.in_progress: [SessionStatus.completed],
    SessionStatus.completed: [],
    SessionStatus.cancelled: [],
}

def create_session(
    db: Session,
    mentor_id,
    learner: User,
    payload: SessionCreate
) -> BookingSession:
    if str(mentor_id) == str(learner.id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot book a session with yourself"
        )

    skill = db.get(Skill, payload.skill_id)
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )

    if str(skill.user_id) != str(mentor_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Skill does not belong to this mentor"
        )

    if not is_within_availability(db, mentor_id, payload.start_time, payload.end_time):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Requested time is outside mentor availability"
        )

    if has_scheduling_conflict(db, mentor_id, payload.start_time, payload.end_time):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Mentor already has a session booked at this time"
        )

    session = BookingSession(
        mentor_id=mentor_id,
        learner_id=learner.id,
        skill_id=payload.skill_id,
        start_time=payload.start_time,
        end_time=payload.end_time,
        note=payload.note
    )

    db.add(session)
    db.commit()
    db.refresh(session)
    return session

def update_session_status(
    db: Session,
    session_id,
    new_status: SessionStatus,
    current_user: User
) -> BookingSession:
    session = db.get(BookingSession, session_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    if str(current_user.id) not in [str(session.mentor_id), str(session.learner_id)]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not part of this session"
        )

    allowed_transitions = VALID_TRANSITIONS.get(session.status, [])
    if new_status not in allowed_transitions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot transition from {session.status.value} to {new_status.value}"
        )

    session.status = new_status
    db.commit()
    db.refresh(session)
    return session