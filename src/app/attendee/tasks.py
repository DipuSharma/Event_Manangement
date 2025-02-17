import logging
from src.worker.celery_worker import celery_app
from src.modals.attendee import Attendee
from src.modals.event import Event, EventStatus
from src.app.attendee.schema import AttendeeUpdate, CheckInResponse
from pydantic import BaseModel
from datetime import datetime
from src.configuration.db_setting import SessionLocal

logger = logging.getLogger(__name__)


@celery_app.task(bind=True)
def check_in_attendee_task(self, attendee_id: int) -> CheckInResponse:
    try:
        logger.info("Checking in attendee with ID %d", attendee_id)
        attendee = Attendee.get(attendee_id=attendee_id)
        attendee = (
            session.query(Attendee)
            .join(Event)
            .filter(Event.status.in_([EventStatus.SCHEDULED, EventStatus.ONGOING]))
            .first()
        )
        if not attendee:
            return CheckInResponse(message="Attendee not found")
        event = attendee.event
        if event.status != EventStatus.SCHEDULED:
            return CheckInResponse(message="Event is not scheduled")
        if event.max_attendees and event.attendees.count() >= event.max_attendees:
            return CheckInResponse(message="Event is full")
        if event.status == EventStatus.COMPLETED:
            return CheckInResponse(message="Event is completed")
        attendee.check_in_status = True
        attendee.save()
        logger.info("Attendee %d checked in successfully", attendee_id)
        return CheckInResponse(message="Attendee checked in successfully")
    except SQLAlchemyError as db_err:
        logger.error("Database error: %s", str(db_err))
        return CheckInResponse(message="Database error occurred")
    except Exception as e:
        logger.exception("Unexpected error")
        return CheckInResponse(message=str(e))


@celery_app.task(bind=True)
def auto_update_event_status(self) -> dict:
    """
    Automatically check and update status of all events based on their start and end times.
    This task should be scheduled to run periodically (e.g., every minute).
    """
    try:
        print("auto_update_event_status________________________________")
        current_time = datetime.now()
        updated_events = []
        session = SessionLocal()

        events = (
            session.query(Event)
            .filter(Event.status.in_([EventStatus.SCHEDULED, EventStatus.ONGOING]))
            .all()
        )

        for event in events:
            if (
                event.status == EventStatus.SCHEDULED
                and event.start_time
                and event.start_time <= current_time
            ):
                event.status = EventStatus.ONGOING
                updated_events.append({"event_id": event.event_id, "status": "started"})
            if (
                event.status == EventStatus.ONGOING
                and event.end_time
                and event.end_time <= current_time
            ):
                event.status = EventStatus.COMPLETED
                updated_events.append(
                    {"event_id": event.event_id, "status": "completed"}
                )
        if updated_events:
            session.commit()

        print("Event statuses updated successfully.")
        return {
            "message": "Event statuses updated successfully",
            "updated_events": updated_events,
        }

    except Exception as e:
        print(f"Error updating event statuses: {str(e)}")
        return {"message": f"Error updating event statuses: {str(e)}"}
