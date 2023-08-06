from typing import Optional, Union

from pydantic import validator

from models.base import BaseSchema


class PsychologistBase(BaseSchema):
    name: str
    specializations: Optional[list[str]] = []
    tg_link: str
    age: int
    description: str
    photo: str
    meet_price: int
    likes: int
    approved: bool


class PsychologistIn(PsychologistBase):
    id: Optional[int]


class PsychologistOut(PsychologistBase):
    id: int
    photo: Union[str]


class ChoosePsychologist(BaseSchema):
    psychologist_id: int
    phone_number: Optional[str]
    tg_link: Optional[str]

