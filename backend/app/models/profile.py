from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class CandidateProfile(Base):
    __tablename__ = 'candidate_profiles'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(index=True, nullable=False)
    location: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(20))
    bio: Mapped[str | None] = mapped_column(Text)
    profile_completeness: Mapped[int] = mapped_column(default=0)

    # Career targets
    target_roles: Mapped[str | None] = mapped_column(Text)  # JSON array as string
    preferred_locations: Mapped[str | None] = mapped_column(Text)
    min_salary: Mapped[int | None] = mapped_column()
    max_salary: Mapped[int | None] = mapped_column()
    experience_level: Mapped[str | None] = mapped_column(String(50))
