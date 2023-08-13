from models.base import BaseSchema


class SpecializationBase(BaseSchema):
    id: int
    name: str


class SpecializationIn(SpecializationBase):
    pass


class SpecializationOut(SpecializationBase):
    pass
