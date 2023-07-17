import logging
import time

import uvicorn
from fastapi import FastAPI
from fastapi import Request

from apis.app.api.middlewares import authenticate
from apis.app.api.routes import api
from core.app_events import start_app, stop_app
from core.config import config

logger = logging.getLogger("uvicorn.error")


def get_application() -> FastAPI:
    application = FastAPI(
        title=config.SERVICE_NAME,
        description=config.DESCRIPTION,
        debug=config.DEBUG,
    )
    application.add_event_handler("startup", start_app)
    application.add_event_handler("shutdown", stop_app)

    application.include_router(api.psychologists_router, prefix=config.API_V1_STR)

    return application


app = get_application()


# app.middleware("http")(authenticate)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
