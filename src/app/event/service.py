from src.modals.event import Event
from src.app.event.schema import EventDisplay
from src.utils.enums import EventStatus


async def create_event(payload=None, db=None):
    get_event = (
        db.query(Event)
        .filter(
            Event.name == payload.name,
            Event.status != EventStatus.CANCELED,
            Event.location == payload.location,
        )
        .first()
    )
    if get_event:
        return {}, "Event already exists"
    event = Event(**payload.dict())
    db.add(event)
    db.commit()
    db.refresh(event)
    return EventDisplay.from_orm(event), "Event create Successfully"


async def update_event(payload=None, db=None):
    event = db.query(Event).filter(Event.event_id == payload.event_id).first()
    for var, value in vars(payload).items():
        setattr(event, var, value) if value else None
    try:
        db.add(event)
        db.commit()
        db.refresh(event)
        return EventDisplay.from_orm(event), "Update successfully"
    except Exception as e:
        return {"message": str(e)}


async def get_events(
    status=None, location=None, start_date=None, end_date=None, db=None
):
    query = db.query(Event).filter(Event.status != EventStatus.CANCELED)
    if status:
        query = query.filter(Event.status == status)
    if location:
        query = query.filter(Event.location.ilike(f"%{location}%"))
    if start_date and end_date:
        query = query.filter(Event.start_date >= start_date, Event.end_date <= end_date)
    events = query.all()
    return [
        EventDisplay.from_orm(event) for event in events
    ], "Event fetched successfully"


async def delete_event(id=None, db=None):
    event = db.query(Event).filter(Event.event_id == id).first()
    if not event:
        return {"message": "Event not found"}
    db.query(Event).filter(Event.event_id == id).delete()
    db.commit()
    return {}, "Event deleted successfully"
