from fastapi import APIRouter, Depends, File, UploadFile
from src.api.attendee.schema import AttendeeCreate, AttendeeUpdate
from src.api.attendee import service as attendee_service
from src.configuration.db_setting import get_db
from sqlalchemy.orm import Session
from src.api.auth.service import get_current_user
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
    response = await attendee_service.delete_attendee(id, db)
    return response


@router.get("/get-attendees")
async def get_attendees(db: Session = Depends(get_db)):
    response = await attendee_service.get_attendees(db)
    return response


@router.get("/logged-user")
async def logged_user(
    db: Session = Depends(get_db), current_user: str = Depends(get_current_user)
):
    response = await attendee_service.get_attendee(current_user["attendee_id"], db)
    return ResponseModel(data=response, message="User fetched successfully")


@router.get("/get-attendee/{id}")
async def get_attendee(
    id: int, db: Session = Depends(get_db), token: str = Depends(get_current_user)
):
    response = await attendee_service.get_attendee(id, db)
    return ResponseModel(data=response, message="User fetched successfully")


@router.post("/upload-attendee")
async def upload_attendee(file: UploadFile = File(...), db: Session = Depends(get_db)):
    response = await attendee_service.bulk_checkin_attendees(file, db)
    return ResponseModel(data=response, message="Attendees checked in successfully")
