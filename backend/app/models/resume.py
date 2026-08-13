from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Resume(Base):
    __tablename__ = 'resumes'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(index=True, nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(Text, nullable=False)
    is_primary: Mapped[bool] = mapped_column(default=False)
    status: Mapped[str] = mapped_column(String(50), default='pending')  # pending, processing, ready, failed
    extracted_data: Mapped[str | None] = mapped_column(Text)  # JSON as string
    created_at: Mapped[str] = mapped_column(String(50), default='2026-08-13T00:00:00Z')
