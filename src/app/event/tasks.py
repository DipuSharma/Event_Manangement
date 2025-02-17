from src.worker.celery_worker import celery_app
from src.modals.event import Event
from src.utils.enums import EventStatus
from datetime import datetime


@celery_app.task(bind=True)
def status_changed_event(self) -> dict:
    try:
        current_time = datetime.now()
        events = Event.filter(status__in=[EventStatus.SCHEDULED, EventStatus.ONGOING])
        for event in events:
            if (
                event.status == EventStatus.CANCELED
                or event.status == EventStatus.COMPLETED
            ):
                continue
            if (
                event.start_time
                and abs((event.start_time - current_time).total_seconds()) < 60
            ):
                event.status = EventStatus.ONGOING
                event.save()
                print(f"Event {event.id} has started")
            if (
                event.end_time
                and abs((event.end_time - current_time).total_seconds()) < 60
            ):
                event.status = EventStatus.COMPLETED
                event.save()
                print(f"Event {event.id} has completed")

        return {"message": "Event statuses updated successfully"}

    except Exception as e:
        return {"message": str(e)}
