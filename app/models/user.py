from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
import uuid
from app.models.base import Base

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.skill import Skill
    from app.models.endorsement import Endorsement
    from app.models.availability import Availability
    from app.models.session import BookingSession

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    skills: Mapped[list["Skill"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    endorsements_given: Mapped[list["Endorsement"]] = relationship(
        foreign_keys="Endorsement.endorser_id",
        back_populates="endorser",
        cascade="all, delete-orphan"
    )
    availabilities: Mapped[list["Availability"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    sessions_as_mentor: Mapped[list["BookingSession"]] = relationship(
        foreign_keys="BookingSession.mentor_id",
        cascade="all, delete-orphan"
    )
    sessions_as_learner: Mapped[list["BookingSession"]] = relationship(
        foreign_keys="BookingSession.learner_id",
        cascade="all, delete-orphan"
    )
