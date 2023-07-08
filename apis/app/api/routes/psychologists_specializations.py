import sys
from http.client import UNPROCESSABLE_ENTITY

from dependency_injector import containers, providers
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Query, HTTPException

from db.repositories.psychologists import PsychologistRepository
from db.repositories.psychologists_specializations import PsychologistSpecializationsRepository

router = APIRouter()


class Container(containers.DeclarativeContainer):

    psychologists_specializations = providers.Factory(PsychologistSpecializationsRepository)

    psychologists = providers.Factory(PsychologistRepository)


@router.get("/psychologists/{specializations_ids}")
@inject
async def psychologists_with_specializations(ids: list[int] = Query(None),
                                            psychologists_specializations: PsychologistSpecializationsRepository = Depends(
                                            Provide[Container.psychologists_specializations]),
                                            psychologist_repo: PsychologistRepository = Depends(Provide[Container.psychologists])) -> list:
    psychologist = await psychologists_specializations.list_with_specializations(ids, psychologist_repo)
    return psychologist


container = Container()
container.wire(modules=[sys.modules[__name__]])
