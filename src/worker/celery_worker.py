from celery import Celery
from src.configuration.settings import setting
from celery.schedules import crontab

# Create Celery app
celery_app = Celery(
    "worker",
    broker=setting.CELERY_BROKER_URL,
    backend=setting.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    result_expires=3600,
    broker_connection_retry_on_startup=True,
)

# Define periodic tasks using Celery Beat
celery_app.conf.beat_schedule = {
    "delete-inactive-companies": {
        "task": "src.api.event.tasks.status_changed_event",
        "schedule": crontab(minute="*"),
    },
    "update-event-statuses": {
        "task": "src.api.attendee.tasks.auto_update_event_status",
        "schedule": crontab(minute="*"),
    },
}

# Load tasks from all modules in the application
celery_app.autodiscover_tasks(
    [
        "src.api.event.tasks",
        "src.api.attendee.tasks",
    ]
)
