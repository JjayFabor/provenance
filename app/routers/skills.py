from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.models.skill import Skill
from app.models.user import User
from app.schemas.skill import SkillCreate, SkillResponse
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/skills", tags=["skills"])

@router.post("/", response_model=SkillResponse, status_code=status.HTTP_201_CREATED)
def create_skill(
    payload: SkillCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    skill = Skill(
        user_id=current_user.id,
        name=payload.name,
        description=payload.description
    )
    db.add(skill)
    try:
        db.commit()
        db.refresh(skill)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Skill already exists."
        )
    
    return skill

@router.get("/", response_model=list[SkillResponse])
def get_skills(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    skills = db.execute(select(Skill)).scalars().all()
    return skills

@router.get("/{skill_id}", response_model=SkillResponse)
def get_skill(
    skill_id,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    skill = db.get(Skill, skill_id)
    if not skill:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Skill not found"
        )
    return skill