from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Job(Base):
    __tablename__ = 'jobs'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    external_id: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    company: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str] = mapped_column(String(255))
    salary_min: Mapped[int | None] = mapped_column()
    salary_max: Mapped[int | None] = mapped_column()
    description: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str] = mapped_column(String(100))
    employment_type: Mapped[str] = mapped_column(String(50))
    seniority_level: Mapped[str | None] = mapped_column(String(50))
    parsed_data: Mapped[str | None] = mapped_column(Text)  # JSON as string
    posted_at: Mapped[str] = mapped_column(String(50))
    fraud_score: Mapped[int | None] = mapped_column(default=0)
