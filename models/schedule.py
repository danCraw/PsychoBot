from models.base import BaseSchema


class ScheduleBase(BaseSchema):
    id: int
    psychologist_id: int
    day_of_the_week: str


class ScheduleIn(ScheduleBase):
    pass


class ScheduleOut(ScheduleBase):
    pass
