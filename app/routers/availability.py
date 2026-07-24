from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import get_db
from app.models.availability import Availability
from app.models.user import User
from app.schemas.availability import AvailabilityCreate, AvailabilityResponse
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/availability", tags=["availability"])

@router.post("/", response_model=AvailabilityResponse, status_code=status.HTTP_201_CREATED)
def create_availability(
    payload: AvailabilityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    availability = Availability(
        user_id=current_user.id,
        start_time=payload.start_time,
        end_time=payload.end_time
    )
    db.add(availability)
    db.commit()
    db.refresh(availability)
    return availability

@router.get("/", response_model=list[AvailabilityResponse])
def get_my_availability(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    availabilities = db.execute(
        select(Availability).where(
            Availability.user_id == current_user.id,
            Availability.is_active == True
        )
    ).scalars().all()
    return availabilities


@router.get("/{user_id}", response_model=list[AvailabilityResponse])
def get_user_availability(
    user_id,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    availabilities = db.execute(
        select(Availability).where(
            Availability.user_id == user_id,
            Availability.is_active == True
        )
    ).scalars().all()
    return availabilities


@router.delete("/{availability_id}", status_code=status.HTTP_204_NO_CONTENT)
def deactivate_availability(
    availability_id,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    availability = db.get(Availability, availability_id)
    if not availability:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Availability not found"
        )
    if str(availability.user_id) != str(current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot modify another user's availability"
        )
    availability.is_active = False
    db.commit()