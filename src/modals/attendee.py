from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from src.configuration.db_setting import Base
from src.utils.enums import UserType


class Attendee(Base):
    __tablename__ = "attendees"
    attendee_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    event_id = Column(Integer, ForeignKey("events.event_id"), nullable=True)
    check_in_status = Column(Boolean, default=True)
    user_type = Column(SQLEnum(UserType), nullable=False, default=UserType.ATTENDEE)
    event = relationship("Event", back_populates="attendees")
