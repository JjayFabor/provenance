from sqlalchemy.orm import Session
from sqlalchemy import select, func
from fastapi import HTTPException, status
from datetime import datetime, timezone, timedelta
from app.models.skill import Skill
from app.models.endorsement import Endorsement
from app.models.user import User
from app.schemas.endorsement import EndorsementCreate

MAX_ENDORSEMENTS_PER_DAY = 10

def get_daily_endorsement_count(db: Session, endorser_id) -> int:
    today_start = datetime.now(timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    count = db.execute(
        select(func.count()).where(
            Endorsement.endorser_id == endorser_id,
            Endorsement.created_at >= today_start
        )
    ).scalar()

    return count or 0

def create_endorsement(
    db: Session,
    skill_id,
    endorser: User,
    payload: EndorsementCreate
) -> Endorsement:
    skill = db.get(Skill, skill_id)
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )
    
    if skill.user_id == endorser.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot endorse your own skill"
        )
    
    existing = db.execute(
        select(Endorsement).where(
            Endorsement.skill_id == skill_id,
            Endorsement.endorser_id == endorser.id
        )
    ).scalars().first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You ahve already endorsed this skill"
        )

    daily_count = get_daily_endorsement_count(db, endorser.id)
    if daily_count >= MAX_ENDORSEMENTS_PER_DAY:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"You have reached the maximum of {MAX_ENDORSEMENTS_PER_DAY} endorsement per day."
        )
    
    endorsement = Endorsement(
        skill_id=skill_id,
        endorser_id=endorser.id,
        rating=payload.rating,
        comment=payload.comment
    )

    db.add(endorsement)
    db.flush()

    recalculate_credibility_score(db, skill)

    db.commit()
    db.refresh(endorsement)
    return endorsement

def recalculate_credibility_score(db: Session, skill: Skill):
    one_year_ago = datetime.now(timezone.utc) - timedelta(days=365)

    endorsements = db.execute(
        select(Endorsement).where(
            Endorsement.skill_id == skill.id
        )
    ).scalars().all()

    if not endorsements:
        skill.credibility_score = 0.0
        return
    
    total_weight = 0.0
    weighted_sum = 0.0

    for e in endorsements:
        weight = 1.0 if e.created_at >= one_year_ago else 0.5
        weighted_sum += e.rating * weight
        total_weight += weight

    skill.credibility_score = round(weighted_sum / total_weight, 2)
    db.add(skill)

