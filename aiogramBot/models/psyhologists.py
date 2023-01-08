from aiogramBot.models.base import BaseSchema


class PsychologistBase(BaseSchema):
    id: int
    name: str
    tg_link: str
    age: int
    description: str
    photo: str
    meet_price: int


class PsychologistIn(PsychologistBase):
    pass


class PsychologistOut(PsychologistBase):
    pass
