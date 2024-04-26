from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

from ref_templates import templates
from dependencias import usuario_atual_site
from apps.usuario import modelos as md_usuario

rota = APIRouter()


@rota.get("/", response_class=HTMLResponse, name="site-index")
def index(
    request: Request, usuario_atual: md_usuario.Usuario = Depends(usuario_atual_site)
) -> HTMLResponse:
    dados = {"request": request, "usuario_atual": usuario_atual}
    return templates.TemplateResponse(name="index/index.html", context=dados)
