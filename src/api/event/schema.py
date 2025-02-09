from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from src.utils.enums import EventStatus


class EventBase(BaseModel):
    name: Optional[str] = Field(default=None, description="Name of the event")
    description: Optional[str] = Field(
        default=None, description="Description of the event"
    )
    start_time: Optional[datetime] = Field(
        default=None, description="Start time of the event"
    )
    end_time: Optional[datetime] = Field(
        default=None, description="End time of the event"
    )
    location: Optional[str] = Field(default=None, description="Location of the event")
    max_attendees: Optional[int] = Field(
        default=None, description="Maximum number of attendees"
    )

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class EventCreate(EventBase):
    pass

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Event 1",
                "description": "This is a description of the event",
                "start_time": "2025-02-09T00:00:00",
                "end_time": "2025-02-10T00:00:00",
                "location": "Location 1",
                "max_attendees": 100,
            }
        }


class EventUpdate(EventBase):
    event_id: int = Field(..., description="Event id")
    pass

    class Config:
        json_schema_extra = {
            "example": {
                "event_id": 1,
                "name": "Event 1",
                "description": "This is a description of the event",
                "start_time": "2025-02-09T00:00:00",
                "end_time": "2025-02-10T00:00:00",
                "location": "Location 1",
                "max_attendees": 100,
            }
        }


class EventDisplay(EventBase):
    event_id: int = Field(..., description="Event id")
    pass


class EventFilters(BaseModel):
    status: Optional[EventStatus] = Field(
        default=None, description="Status of the event"
    )
    location: Optional[str] = Field(default=None, description="Location of the event")
    start_date: Optional[datetime] = Field(
        default=None, description="Start date of the event"
    )
    end_date: Optional[datetime] = Field(
        default=None, description="End date of the event"
    )
