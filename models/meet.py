from datetime import time
from typing import Optional
from models.base import BaseSchema


class MeetBase(BaseSchema):
    id: int
    time_start: time
    time_end: time
    day_of_the_week_id: int
    client_id: Optional[int]


class MeetIn(MeetBase):
    pass


class MeetOut(MeetBase):
    pass
