import sys
from typing import List
from http.client import UNPROCESSABLE_ENTITY
from fastapi import APIRouter, HTTPException, Depends
from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide

from db.base import redis_conn
from db.repositories.psychologists import PsychologistRepository
from db.repositories.psychologists_specializations import PsychologistSpecializationsRepository
from db.repositories.specializations import SpecializationRepository
from models.psychologist import PsychologistIn, PsychologistOut, ChoosePsychologist

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
    psychologist = await psychologist_repo.approved_psychologists(specializations_repo._table, psychologists_specializations_repo._table)
    return psychologist


@router.get("/{psychologist_id}")
@inject
async def one_psychologist(psychologist_id: int, psychologist_repo: PsychologistRepository = Depends(
                           Provide[Container.psychologists])) -> PsychologistOut:
    psychologist = await psychologist_repo.get(psychologist_id)
    if psychologist:
        return psychologist
    else:
        raise HTTPException(status_code=UNPROCESSABLE_ENTITY, detail="psychologist with the given Id not found")


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
                              Provide[Container.psychologists])) -> List[PsychologistOut]:
    await redis_conn
    psychologist = await psychologist_repo.delete(psychologist_id)
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


container = Container()
container.wire(modules=[sys.modules[__name__]])
