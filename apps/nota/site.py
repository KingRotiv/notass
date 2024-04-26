from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse

from ref_templates import templates
from dependencias import usuario_atual_site
from apps.nota import esquemas as eq
from apps.usuario import modelos as md_usuario


rota = APIRouter(prefix="/nota", tags=["Nota"])


@rota.get("/", response_class=HTMLResponse, name="site-nota")
def nota(
    request: Request,
    usuario_atual: md_usuario.Usuario = Depends(usuario_atual_site),
) -> HTMLResponse:
    if not usuario_atual:
        url = request.url_for("site-usuario-entrar").include_query_params(
            prox=request.url.path
        )
        return RedirectResponse(url=url)
    dados = {
        "request": request,
        "usuario_atual": usuario_atual,
        "filtro_ordem": eq.FiltroPesquisaOrdem,
    }
    return templates.TemplateResponse(name="nota/index.html", context=dados)
