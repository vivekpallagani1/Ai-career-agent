from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Application(Base):
    __tablename__ = 'applications'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(index=True, nullable=False)
    job_id: Mapped[int] = mapped_column(index=True, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default='saved')  # discovered, saved, preparing, applied, screening, interview, offer, rejected
    resume_used: Mapped[int | None] = mapped_column()  # resume ID
    match_score: Mapped[int] = mapped_column(default=0)
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[str] = mapped_column(String(50))
    updated_at: Mapped[str] = mapped_column(String(50))
