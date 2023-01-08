from aiogramBot.models.base import BaseSchema
from aiogramBot.models.psyhologists import PsychologistBase


class ScheduleBase(BaseSchema):
    id: int
    psychologist_id: int
    day_of_the_week: str


class ScheduleIn(ScheduleBase):
    pass


class ScheduleOut(ScheduleBase):
    pass
