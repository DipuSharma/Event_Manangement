from pydantic import BaseModel, Field
from typing import Optional


class AttendeeBase(BaseModel):
    first_name: Optional[str] = Field(
        default=None, description="First name of the attendee"
    )
    last_name: Optional[str] = Field(
        default=None, description="Last name of the attendee"
    )
    email: Optional[str] = Field(default=None, description="Email of the attendee")
    phone_number: Optional[str] = Field(
        default=None, description="Phone number of the attendee"
    )
    event_id: Optional[int] = Field(
        default=None, description="Event id of the attendee"
    )

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class AttendeeCreate(AttendeeBase):
    pass


class AttendeeUpdate(AttendeeBase):
    attendee_id: int = Field(default=None, description="ID of the attendee")
    pass


class AttendeeDisplay(AttendeeBase):
    attendee_id: int = Field(default=None, description="ID of the attendee")
    user_type: str = Field(default=None, description="User type")
    pass


class CheckInResponse(BaseModel):
    message: str