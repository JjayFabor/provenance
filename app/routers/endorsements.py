from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.models.endorsement import Endorsement
from app.models.user import User
from app.schemas.endorsement import EndorsementCreate, EndorsementResponse
from app.core.dependencies import get_current_user
from app.services.endorsement_service import create_endorsement

router = APIRouter(prefix="/skills", tags=["endorsements"])

@router.post("/{skill_id}/endorsements", response_model=EndorsementResponse, status_code=status.HTTP_201_CREATED)
def endorse_skill(
    skill_id,
    payload: EndorsementCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_endorsement(db, skill_id, current_user, payload)

@router.get("/{skill_id}/endorsements", response_model=list[EndorsementResponse])
def get_skill_endorsement(
    skill_id,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    endorsements = db.execute(
        select(Endorsement).where(
            Endorsement.skill_id == skill_id
        )
    ).scalars().all()

    return endorsements