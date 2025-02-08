from src.api.auth.schema import UserDisplay, UserLogin
from src.utils.common import EncryptedPassword as _password
from sqlalchemy.orm import Session
from src.configuration.db_setting import SessionLocal
from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timezone, timedelta
from src.configuration.settings import setting
from src.modals.attendee import Attendee
from src.api.auth.schema import UserRegister, TokenResponse, UserDisplay
from src.utils.enums import UserType

JWT_SECRET = setting.SECRET_KEY
JWT_ALGORITHM = setting.ALGORITHM
oauth2_scheme = HTTPBearer()


async def decode_token(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        exp = decoded_token.get("exp")
        sub = decoded_token.get("sub")
        if exp is None or sub is None:
            return None
        exp_datetime = datetime.fromtimestamp(exp, tz=timezone.utc)
        current_time = datetime.now(tz=timezone.utc)

        if exp_datetime >= current_time:
            return sub
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, details="Session expired"
            )
    except JWTError:
        return None


async def register_user(user: UserRegister, db: Session):
    hashed_password = _password.get_hash_passssword(user.password)
    del user.password
    user.password = hashed_password
    data = Attendee(
        email=user.email,
        password=hashed_password,
        user_type=UserType.ADMIN,
    )
    try:
        db.add(data)
        db.commit()
        db.refresh(data)
        return UserDisplay.from_orm(data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_226_IM_USED,
            detail="User already exists",
        )


async def login_user(email: str, password: str, db: Session):
    user = db.query(Attendee).filter(Attendee.email == email).first()
    if not user:
        return {"message": "User not found"}
    if not _password.verify_hash_password(password, user.password):
        return {"message": "Invalid password"}
    expires_delta = timedelta(minutes=60)
    generate_token = jwt.encode(
        {"sub": user.email, "exp": datetime.now() + expires_delta},
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )
    return TokenResponse(access_token=generate_token, token_type="bearer")


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
):
    token = credentials.credentials
    try:
        decoded_token = await decode_token(token=token)
        if decoded_token:
            session = SessionLocal()
            user = (
                session.query(Attendee).filter(Attendee.email == decoded_token).first()
            )
            return {
                "attendee_id": user.attendee_id,
                "email": user.email,
                "user_type": user.user_type,
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Token {e}"
        )



