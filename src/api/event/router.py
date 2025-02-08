from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.configuration.db_setting import get_db
from src.api.auth.service import get_current_user
from src.modals.event import Event

router = APIRouter()


@router.post("/create-event")
def create_event(db: Session = Depends(get_db), token: str = Depends(get_current_user)):
    # db.add(event)
    # db.commit()
    # db.refresh(event)
    # return event

    return {}
