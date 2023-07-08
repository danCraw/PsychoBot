from models.base import BaseSchema


class ClientBase(BaseSchema):
    tg_id: int
    name: str
    tariff_id: str
    remaining_meets: int


class ClientIn(ClientBase):
    pass


class ClientOut(ClientBase):
    pass
