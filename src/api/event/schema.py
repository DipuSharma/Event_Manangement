from pydantic import BaseModel, Field
from typing import Optional


class EventBase(BaseModel):
    name: Optional[str] = Field(default=None, description="Name of the event")
    description: Optional[str] = Field(
        default=None, description="Description of the event"
    )
    start_time: Optional[str] = Field(
        default=None, description="Start time of the event"
    )
    end_time: Optional[str] = Field(default=None, description="End time of the event")
    location: Optional[str] = Field(default=None, description="Location of the event")
    max_attendees: Optional[int] = Field(
        default=None, description="Maximum number of attendees"
    )

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class EventCreate(EventBase):
    pass


class EventUpdate(EventBase):
    pass


class EventDisplay(EventBase):
    pass
