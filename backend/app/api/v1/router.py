from fastapi import APIRouter

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.jobs import router as jobs_router
from app.api.v1.endpoints.profiles import router as profiles_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(health_router)
router.include_router(jobs_router)
router.include_router(profiles_router)


@router.get('/ping')
async def ping() -> dict:
    return {'message': 'pong'}
