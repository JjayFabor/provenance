from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import select, or_
from app.database import get_db
from app.models.session import BookingSession
from app.models.user import User
from app.schemas.session import SessionCreate, SessionResponse, SessionStatusUpdate
from app.core.dependencies import get_current_user
from app.services.session_service import create_session, update_session_status

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("/{mentor_id}", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def book_session(
    mentor_id,
    payload: SessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_session(db, mentor_id, current_user, payload)


@router.get("/", response_model=list[SessionResponse])
def get_my_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sessions = db.execute(
        select(BookingSession).where(
            or_(
                BookingSession.mentor_id == current_user.id,
                BookingSession.learner_id == current_user.id
            )
        )
    ).scalars().all()
    return sessions


@router.patch("/{session_id}/status", response_model=SessionResponse)
def change_session_status(
    session_id,
    payload: SessionStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_session_status(db, session_id, payload.status, current_user)