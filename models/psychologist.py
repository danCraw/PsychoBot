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


class PsychologistOut(PsychologistBase, extra='allow'):
    id: int
    photo: Union[str]
    content: Optional[str]

    @validator("photo", always=True)
    def photo_path(cls, v):
        return "".join(['/media/', v]) if '/media/' not in v else v


    @validator("content", always=True)
    @classmethod
    def content_field(cls, v, values):
        if v is None:
            with open(values['photo'], 'rb') as photo:
                return str(photo.read())
        else:
            return v


class ChoosePsychologist(BaseSchema):
    psychologist_id: int
    phone_number: Optional[str]
    tg_link: Optional[str]

