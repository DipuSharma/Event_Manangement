from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from src.configuration.db_setting import get_db
from src.api.auth.service import get_current_user
from src.api.event import service as event_service
from src.api.event.schema import EventUpdate, EventCreate, EventFilters
from src.utils.response import ResponseModel

router = APIRouter()


@router.post("/create-event")
async def create_event(
    payload: EventCreate,
    db: Session = Depends(get_db),
    token: str = Depends(get_current_user),
):
    response, msg = await event_service.create_event(payload, db)
    if response:
        return ResponseModel(data=response, message=msg)

    return ResponseModel(data={}, message=msg)


@router.put("/update-event")
async def update_event(
    payload: EventUpdate,
    db: Session = Depends(get_db),
    token: str = Depends(get_current_user),
):
    response, msg = await event_service.update_event(payload, db)
    return ResponseModel(data=response, message=msg)


@router.get("/get-events")
async def get_events(
    filter: EventFilters = Depends(),
    db: Session = Depends(get_db),
    token: str = Depends(get_current_user),
):
    response, msg = await event_service.get_events(**filter.dict(), db=db)
    return ResponseModel(data=response, message=msg)


@router.delete("/delete-event/{id}")
async def delete_event(
    id: int, db: Session = Depends(get_db), token: str = Depends(get_current_user)
):
    response, msg = await event_service.delete_event(id, db)
    return ResponseModel(data=response, message=msg)
