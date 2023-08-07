import sys
from http.client import UNPROCESSABLE_ENTITY, OK
from typing import List

from aio_pika import Message
from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse

from core.base_config import config
from db.repositories.psychologists import PsychologistRepository
from db.repositories.psychologists_specializations import PsychologistSpecializationsRepository
from db.repositories.specializations import SpecializationRepository
from models.psychologist import PsychologistIn, PsychologistOut, ChoosePsychologist
from rabbit.base import rabbit

router = APIRouter()


class Container(containers.DeclarativeContainer):

    psychologists = providers.Factory(PsychologistRepository)

    psychologists_specializations = providers.Factory(PsychologistSpecializationsRepository)

    specializations = providers.Factory(SpecializationRepository)


@router.get("/")
@inject
async def psychologists_list(psychologist_repo: PsychologistRepository = Depends(Provide[Container.psychologists]),
                             psychologists_specializations_repo: PsychologistSpecializationsRepository = Depends(
                                 Provide[Container.psychologists_specializations]),
                             specializations_repo: SpecializationRepository = Depends(
                                 Provide[Container.specializations])
                             ) -> List[PsychologistOut]:
    psychologists = await psychologist_repo.psychologists_list(specializations_repo._table,
                                                              psychologists_specializations_repo._table)
    return psychologists


# @router.get("/{psychologist_id}")
# @inject
# async def one_psychologist(psychologist_id: int, psychologist_repo: PsychologistRepository = Depends(
#                            Provide[Container.psychologists])) -> PsychologistOut:
#     psychologist = await psychologist_repo.get(psychologist_id)
#     if psychologist:
#         return psychologist
#     else:
#         raise HTTPException(status_code=UNPROCESSABLE_ENTITY, detail="psychologist with the given Id not found")


@router.post("/")
@inject
async def create_psychologist(psychologist: PsychologistIn, psychologist_repo: PsychologistRepository = Depends(
                              Provide[Container.psychologists])) -> PsychologistOut:
    psychologist = await psychologist_repo.create(psychologist)
    return psychologist


@router.put("/")
@inject
async def update_psychologist(psychologist: PsychologistIn, psychologist_repo: PsychologistRepository = Depends(
                              Provide[Container.psychologists])) -> PsychologistOut:
    psychologist.approved = False
    psychologist = await psychologist_repo.update(psychologist)
    if psychologist:
        return psychologist
    else:
        raise HTTPException(status_code=UNPROCESSABLE_ENTITY, detail="psychologist with the given Id not found")


@router.post("/choose/{psychologist_id}")
@inject
async def choose_psychologist(choose_psychologist: ChoosePsychologist, psychologist_repo: PsychologistRepository = Depends(
                              Provide[Container.psychologists])) -> int:
    async def _send_msg_to_admins_tg():
        tg_link = choose_psychologist.tg_link if choose_psychologist.tg_link else '-'
        phone_number = choose_psychologist.phone_number if choose_psychologist.phone_number else '-'
        await rabbit.channel.default_exchange.publish(
            Message(
                body=f'Клиент выбрал психолога Имя: {psychologist.name} Телеграм: {psychologist.tg_link}.'
                     f'\nКонтакты клиента: Телеграм: {tg_link} Номер телефона: {phone_number}'.encode(encoding='utf-8')),
            routing_key=config.routing_key,
        )

    psychologist = await psychologist_repo.get(choose_psychologist.psychologist_id)
    if psychologist:
        await _send_msg_to_admins_tg()
        return OK
    else:
        raise HTTPException(status_code=UNPROCESSABLE_ENTITY, detail="psychologist with the given Id not found")


@router.post("/choose/{psychologist_id}")
@inject
async def choose_psychologist(choose_psychologist: ChoosePsychologist, psychologist_repo: PsychologistRepository = Depends(
                              Provide[Container.psychologists])) -> List[PsychologistOut]:
    await rabbit.connection.default_exchange.publish(
        Message(
            body='Кто-то выбрал психолога'.encode(encoding='utf-8')),
        routing_key=config.routing_key,
    )
    queue = rabbit.queue
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                print(message.body)

    psychologist = await psychologist_repo.delete(choose_psychologist.psychologist_id)
    if psychologist:
        return psychologist
    else:
        raise HTTPException(status_code=UNPROCESSABLE_ENTITY, detail="psychologist with the given Id not found")


@router.delete("/{psychologist_id}")
@inject
async def delete_psychologist(psychologist_id: int, psychologist_repo: PsychologistRepository = Depends(
                              Provide[Container.psychologists])) -> List[PsychologistOut]:
    psychologist = await psychologist_repo.delete(psychologist_id)
    if psychologist:
        return psychologist
    else:
        raise HTTPException(status_code=UNPROCESSABLE_ENTITY, detail="psychologist with the given Id not found")


@router.get("/media/{image_path}")
@inject
async def media_file(image_path: str):
    return FileResponse('/media/' + image_path)


@router.get("/{image_path}")
@inject
async def media_file(image_path: str):
    return FileResponse('/media/' + image_path)

container = Container()
container.wire(modules=[sys.modules[__name__]])
