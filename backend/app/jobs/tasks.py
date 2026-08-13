from app.jobs.celery_app import celery_app


@celery_app.task
def process_job_feed() -> str:
    return 'job feed refreshed'
