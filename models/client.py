from models.base import BaseSchema


class ClientBase(BaseSchema):
    tg_id: str
    name: str
    tariff_id: str
    remaining_meets: int


class ClientIn(ClientBase):
    pass


class ClientOut(ClientBase):
    pass
