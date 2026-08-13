from celery import Celery

from app.core.config import settings

celery_app = Celery(
    'career_agent',
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.task_routes = {'app.jobs.tasks.*': {'queue': 'default'}}


@celery_app.task
def health_check_task() -> str:
    return 'worker-ok'
