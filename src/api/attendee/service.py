from sqlalchemy.orm import Session
from src.modals.attendee import Attendee
from src.api.attendee.schema import AttendeeDisplay, AttendeeCreate, AttendeeUpdate
from src.utils.enums import UserType


async def create_attendee(payload: AttendeeCreate, db: Session):
    attendee = Attendee(**payload.dict(), user_type=UserType.ATTENDEE)
    db.add(attendee)
    db.commit()
    db.refresh(attendee)
    return AttendeeDisplay.from_orm(attendee)


async def update_attendee(id: int, payload: AttendeeUpdate, db: Session):
    attendee.id = id
    db.merge(attendee)
    db.commit()
    return AttendeeDisplay.from_orm(attendee)


async def delete_attendee(id: int, db: Session):
    db.query(Attendee).filter(Attendee.id == id).delete()
    db.commit()
    return {"message": "Attendee deleted"}


async def get_attendee(id: int, db: Session):
    attendee = db.query(Attendee).filter(Attendee.id == id).first()
    if not attendee:
        return {"message": "Attendee not found"}
    return AttendeeDisplay.from_orm(attendee)


async def get_attendees(db: Session):
    attendees = db.query(Attendee).all()
    return [AttendeeDisplay.from_orm(attendee) for attendee in attendees]
