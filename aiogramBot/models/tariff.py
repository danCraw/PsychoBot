from aiogramBot.models.base import BaseSchema
from aiogramBot.models.psyhologists import PsychologistBase


class TariffBase(BaseSchema):
    name: str
    meets: int


class TariffIn(TariffBase):
    pass


class TariffOut(TariffBase):
    pass
