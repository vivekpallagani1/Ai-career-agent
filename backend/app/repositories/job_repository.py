from sqlalchemy.orm import Session

from app.models.job import Job


class JobRepository:
    def __init__(self, db: Session):
        self.db = db

    def list_jobs(self, limit: int = 20, offset: int = 0) -> list[Job]:
        return self.db.query(Job).limit(limit).offset(offset).all()

    def get_by_id(self, job_id: int) -> Job | None:
        return self.db.query(Job).filter(Job.id == job_id).first()

    def get_by_external_id(self, external_id: str) -> Job | None:
        return self.db.query(Job).filter(Job.external_id == external_id).first()

    def create(self, **kwargs) -> Job:
        job = Job(**kwargs)
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        return job

    def search(self, title: str | None = None, company: str | None = None, location: str | None = None, limit: int = 20) -> list[Job]:
        query = self.db.query(Job)
        if title:
            query = query.filter(Job.title.ilike(f'%{title}%'))
        if company:
            query = query.filter(Job.company.ilike(f'%{company}%'))
        if location:
            query = query.filter(Job.location.ilike(f'%{location}%'))
        return query.limit(limit).all()
