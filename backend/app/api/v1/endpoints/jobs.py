from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.repositories.job_repository import JobRepository
from app.schemas.job import JobMatchScoreResponse, JobResponse
from app.services.job_matching import JobMatchingService

router = APIRouter(prefix='/jobs', tags=['jobs'])


@router.get('/', response_model=list[JobResponse])
async def list_jobs(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    repo = JobRepository(db)
    return repo.list_jobs(limit=limit, offset=offset)


@router.get('/search', response_model=list[JobResponse])
async def search_jobs(
    title: str | None = Query(None),
    company: str | None = Query(None),
    location: str | None = Query(None),
    db: Session = Depends(get_db),
):
    repo = JobRepository(db)
    return repo.search(title=title, company=company, location=location)


@router.get('/{job_id}', response_model=JobResponse)
async def get_job(job_id: int, db: Session = Depends(get_db)):
    repo = JobRepository(db)
    job = repo.get_by_id(job_id)
    if not job:
        return {'error': 'Job not found'}
    return job


@router.post('/{job_id}/match')
async def calculate_job_match(
    job_id: int,
    db: Session = Depends(get_db),
) -> JobMatchScoreResponse:
    # Placeholder: in production, extract user profile and compute match
    repo = JobRepository(db)
    job = repo.get_by_id(job_id)

    service = JobMatchingService()
    candidate_profile = {'name': 'Candidate', 'skills': [], 'experience': []}
    job_dict = {'title': job.title if job else 'Unknown'} if job else {}

    result = service.score_candidate_job(candidate_profile, job_dict)

    return JobMatchScoreResponse(
        job_id=job_id,
        overall_match=result.get('overall_match', 0),
        matched_skills=result.get('matched_skills', []),
        missing_skills=result.get('missing_skills', []),
        explanation=result.get('reasoning', 'Match calculation pending'),
    )
