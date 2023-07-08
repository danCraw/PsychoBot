from models.base import BaseSchema


class TariffBase(BaseSchema):
    name: str
    meets: int


class TariffIn(TariffBase):
    pass


class TariffOut(TariffBase):
    pass
