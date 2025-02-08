from fastapi import APIRouter, Depends
from src.api.auth import service as auth_service
from src.api.auth.service import get_current_user
from src.api.auth.schema import UserLogin, UserRegister
from src.configuration.db_setting import get_db
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/login")
async def login(payload: UserLogin, db: Session = Depends(get_db)):
    response = await auth_service.login_user(
        email=payload.email, password=payload.password, db=db
    )
    return response


@router.post("/register")
async def register(paylaod: UserRegister, db: Session = Depends(get_db)):
    response = await auth_service.register_user(user=paylaod, db=db)
    return response


@router.post("/logout")
def logout():
    pass
