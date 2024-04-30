import os
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from loguru import logger

import config
from db import iniciar_db
from apps.index.site import rota as site_index

from apps.usuario.site import rota as site_usuario
from apps.usuario.api import rota as api_usuario

from apps.nota.site import rota as site_nota
from apps.nota.api import rota as api_nota


full_path = os.path.realpath(__file__)
path = os.path.dirname(full_path)


@asynccontextmanager
async def iniciar(*args):
    iniciar_db()
    logger.add(
        os.path.join(path, "logs", "{time}.log"), rotation="00:00", retention="30 days"
    )
    logger.info("Iniciado")
    yield


app = FastAPI(title=config.NOME_APP, lifespan=iniciar)
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(path, "templates", "static")),
    name="static",
)
app.include_router(site_index, include_in_schema=False)

app.include_router(site_usuario, include_in_schema=False)
app.include_router(api_usuario, prefix="/api")

app.include_router(site_nota, include_in_schema=False)
app.include_router(api_nota, prefix="/api")


if __name__ == "__main__":
    uvicorn.run(app)
