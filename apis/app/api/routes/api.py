from fastapi import APIRouter

from apis.app.api.routes import psychologists
from apis.app.api.routes import psychologists_specializations
from apis.app.api.routes import media

psychologists_router = APIRouter()
psychologists_router.include_router(psychologists.router, prefix="/psychologists")
psychologists_router.include_router(psychologists_specializations.router, prefix="/psychologists_specializations")
psychologists_router.include_router(media.router, prefix="/media")
