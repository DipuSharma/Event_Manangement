from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Optional
from fastapi import HTTPException
import re


class UserRegister(BaseModel):
    email: str = Field(..., description="User email")
    password: str = Field(..., description="User password")
    confirm_password: str = Field(..., description="Confirm user password")

    @field_validator("email")
    def validate_email(cls, v):
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", v):
            raise HTTPException(status_code=400, detail="Invalid email address")
        return v

    @field_validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise HTTPException(
                status_code=400, detail="Password must be at least 8 characters long"
            )
        return v

    @model_validator(mode="before")
    def password_match(cls, values):
        password = values.get("password")
        password1 = values.get("confirm_password")
        if not password == password1:
            raise HTTPException(status_code=400, detail="Passwords do not match")
        return values

    class Config:
        json_schema_extra = {
            "example": {
                "email": "contact@mail.com",
                "password": "secret",
                "confirm_password": "secret",
            }
        }
        populate_by_name = True


class UserLogin(BaseModel):
    email: str = Field(..., description="User email")
    password: str = Field(..., description="User password")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "admin@mail.com",
                "password": "Admin1234@",
            }
        }


class UserDisplay(BaseModel):
    attendee_id: int = Field(default=None, description="User id")
    email: str = Field(default=None, description="User email")
    user_type: str = Field(default=None, description="User type")

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
