from celery import Celery

from src.config import settings

celery_instance = Celery(
    'tasks',
    broker=settings.redis_url,
    include=[
        'src.tasks.tasks',
    ],
)

celery_instance.conf.beat_schedule = {
    'luboe_nazvanie': {
        'task': 'bookings_from_today',
        'schedule': 5,
    }
}