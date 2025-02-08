from enum import Enum


class EventStatus(str, Enum):
    SCHEDULED = "scheduled"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELED = "canceled"

    def __str__(self):
        return self.value


class UserType(str, Enum):
    ADMIN = "admin"
    ATTENDEE = "attendee"

    def __str__(self):
        return self.value
