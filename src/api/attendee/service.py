from sqlalchemy.orm import Session
from src.modals.attendee import Attendee
from src.api.attendee.schema import AttendeeDisplay, AttendeeCreate, AttendeeUpdate
from src.modals.event import Event, EventStatus
from src.utils.enums import UserType
from sqlalchemy import and_, any_, func, or_
from src.utils.common import EncryptedPassword as _password
from src.api.attendee.tasks import check_in_attendee_task
import csv
import io
import re
from fastapi import HTTPException


async def create_attendee(payload: AttendeeCreate, db: Session):
    get_event = (
        db.query(Event)
        .filter(
            and_(
                Event.event_id == payload.event_id, Event.status != EventStatus.CANCELED
            )
        )
        .first()
    )
    if not get_event:
        return {"message": "Event does not exist"}
    current_attendees_count = (
        db.query(Attendee).filter(Attendee.event_id == payload.event_id).count()
    )
    if get_event.max_attendees and current_attendees_count >= get_event.max_attendees:
        return {}, "Event has reached maximum capacity"
    generate_event_password = _password.get_hash_passssword(get_event.name[:5] + "123@")
    attendee = Attendee(
        **payload.dict(), user_type=UserType.ATTENDEE, password=generate_event_password
    )
    db.add(attendee)
    db.commit()
    db.refresh(attendee)
    return (
        AttendeeDisplay.from_orm(attendee),
        f"Attendee create successfully, and default password is {get_event.name[:5] + '123@'}",
    )


async def update_attendee(payload=None, db=None):
    existing_user = (
        db.query(Attendee)
        .filter(
            or_(
                Attendee.email == payload.email,
                Attendee.attendee_id == payload.attendee_id,
            )
        )
        .first()
    )
    if existing_user.user_type not in {UserType.ADMIN}:
        for var, value in vars(payload).items():
            setattr(existing_user, var, value) if value else None
        db.add(existing_user)
        db.commit()
        db.refresh(existing_user)
        return AttendeeDisplay.from_orm(existing_user), "Update successfully"
    else:
        return {"status": False, "message": "Update not successfully"}


async def delete_attendee(id: int, db: Session):
    db.query(Attendee).filter(Attendee.attendee_id == id).delete()
    db.commit()
    return {"message": "Attendee deleted"}


async def get_attendee(id: int, db: Session):
    attendee = db.query(Attendee).filter(Attendee.attendee_id == id).first()
    if not attendee:
        return {"message": "Attendee not found"}
    return AttendeeDisplay.from_orm(attendee), "Attendee fetched successfully"


async def get_attendees(db: Session):
    attendees = db.query(Attendee).all()
    return [
        AttendeeDisplay.from_orm(attendee) for attendee in attendees
    ], "Attendees fetched successfully"


async def bulk_checkin_attendees(file=None, db: Session = None):
    content = file.file.read().decode("utf-8")
    csv_reader = csv.reader(io.StringIO(content))
    task_ids = []
    for row in csv_reader:
        attendee_id = int(row[0])
        task = check_in_attendee_task.delay(attendee_id)
        task_ids.append(task.id)
    return {"message": "Bulk check-in initiated", "task_ids": task_ids}
