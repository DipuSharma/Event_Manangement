from fastapi import APIRouter, Depends, File, UploadFile
from src.app.attendee.schema import AttendeeCreate, AttendeeUpdate, AttendeeFilter
from src.app.attendee import service as attendee_service
from src.configuration.db_setting import get_db
from sqlalchemy.orm import Session
from src.app.auth.service import get_current_user
from src.utils.response import ResponseModel

router = APIRouter()


@router.post("/create-attendee")
async def create_attendee(
    payload: AttendeeCreate,
    db: Session = Depends(get_db),
    token: str = Depends(get_current_user),
):
    response, msg = await attendee_service.create_attendee(payload, db)
    return ResponseModel(data=response, message=msg)


@router.put("/update-attendee")
async def update_attendee(
    payload: AttendeeUpdate,
    db: Session = Depends(get_db),
    token: str = Depends(get_current_user),
):
    response, msg = await attendee_service.update_attendee(payload, db)
    return ResponseModel(data=response, message=msg)


@router.delete("/delete-attendee/{id}")
async def delete_attendee(
    id: int, db: Session = Depends(get_db), token: str = Depends(get_current_user)
):
    response, msg = await attendee_service.delete_attendee(id, db)
    return ResponseModel(data=response, message=msg)


@router.get("/get-attendees")
async def get_attendees(
    filter: AttendeeFilter = Depends(),
    db: Session = Depends(get_db),
    token: str = Depends(get_current_user),
):
    response, msg = await attendee_service.get_attendees(**filter.dict(), db=db)
    return ResponseModel(data=response, message=msg)


@router.get("/get-attendee/{id}")
async def get_attendee(
    id: int, db: Session = Depends(get_db), token: str = Depends(get_current_user)
):
    response, msg = await attendee_service.get_attendee(id, db)
    return ResponseModel(data=response, message=msg)


@router.post("/upload-attendee")
async def upload_attendee(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    token: str = Depends(get_current_user),
):
    response, msg = await attendee_service.bulk_checkin_attendees(file, db)
    return ResponseModel(data=response, message=msg)
