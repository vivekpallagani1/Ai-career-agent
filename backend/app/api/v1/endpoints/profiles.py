from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_db
from app.repositories.profile_repository import ProfileRepository
from app.schemas.profile import ProfileCreateRequest, ProfileResponse

router = APIRouter(prefix='/profiles', tags=['profiles'])


@router.post('/', response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(request: ProfileCreateRequest, db: Session = Depends(get_db)):
    # In a real scenario, extract user_id from JWT token
    user_id = 1  # placeholder
    repo = ProfileRepository(db)
    profile = repo.create(user_id=user_id, **request.model_dump(exclude_unset=True))
    return profile


@router.get('/{profile_id}', response_model=ProfileResponse)
async def get_profile(profile_id: int, db: Session = Depends(get_db)):
    repo = ProfileRepository(db)
    profile = repo.get_by_user_id(profile_id)
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Profile not found')
    return profile
