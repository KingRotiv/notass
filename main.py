import os

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

import config
from db import iniciar_db
from apps.index.site import rota as site_index

from apps.usuario.site import rota as site_usuario
from apps.usuario.api import rota as api_usuario

from apps.nota.site import rota as site_nota
from apps.nota.api import rota as api_nota


full_path = os.path.realpath(__file__)
path = os.path.dirname(full_path)

app = FastAPI(title=config.NOME_APP, lifespan=iniciar_db)
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
