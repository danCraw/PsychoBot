from datetime import datetime, time
from typing import Optional
from aiogramBot.models.base import BaseSchema


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
