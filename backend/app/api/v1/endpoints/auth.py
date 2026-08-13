from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token, hash_password, verify_password
from app.dependencies import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.auth import UserLoginRequest, UserRegisterRequest

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register(request: UserRegisterRequest, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    existing = user_repo.get_by_email(request.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Email already registered',
        )

    hashed = hash_password(request.password)
    user = user_repo.create(
        email=request.email,
        hashed_password=hashed,
        name=request.name,
    )

    access_token = create_access_token(
        data={'sub': user.email, 'user_id': user.id},
        expires_delta=timedelta(minutes=60),
    )

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user': {'id': user.id, 'email': user.email, 'name': user.name},
    }


@router.post('/login')
async def login(request: UserLoginRequest, db: Session = Depends(get_db)):
    user_repo = UserRepository(db)
    user = user_repo.get_by_email(request.email)

    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid email or password',
        )

    access_token = create_access_token(
        data={'sub': user.email, 'user_id': user.id},
        expires_delta=timedelta(minutes=60),
    )

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user': {'id': user.id, 'email': user.email, 'name': user.name},
    }
