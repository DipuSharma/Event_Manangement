from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from src.configuration.db_setting import Base
from src.utils.enums import EventStatus


class Event(Base):
    __tablename__ = "events"
    event_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    location = Column(String, nullable=True)
    max_attendees = Column(Integer, nullable=True)
    status = Column(SQLEnum(EventStatus), nullable=True, default=EventStatus.SCHEDULED)
    attendees = relationship("Attendee", back_populates="event")
