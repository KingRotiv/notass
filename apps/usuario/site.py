from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse

import config
from dependencias import usuario_atual_site
from ref_templates import templates
from utils import seguranca as sq
from apps.usuario import modelos as md_usuario


rota = APIRouter(prefix="/usuario", tags=["Usuário"])


@rota.get("/", response_model=None, name="site-usuario")
def index(
    request: Request,
    usuario_atual: md_usuario.Usuario = Depends(usuario_atual_site),
) -> HTMLResponse | RedirectResponse:
    """
    Página de pefil do usuário atual.
    """
    if not usuario_atual:
        url = request.url_for("site-usuario-entrar").include_query_params(
            prox=request.url.path
        )
        return RedirectResponse(url=url)
    dados = {
        "request": request,
        "usuario_atual": usuario_atual,
        "telegram_bot_nome": config.TELEGRAM_BOT_NOME,
        "regex_senha": config.REGEX_SENHA,
    }
    return templates.TemplateResponse(name="usuario/index.html", context=dados)


@rota.get(
    "/entrar/",
    name="site-usuario-entrar",
    response_model=None,
)
def entrar(
    request: Request,
    usuario_atual: md_usuario.Usuario = Depends(usuario_atual_site),
    prox: str = None,
) -> HTMLResponse | RedirectResponse:
    """
    Página para autenticação de um usuário.
    """
    if usuario_atual:
        return RedirectResponse(url=request.url_for("site-index"))
    prox = sq.validar_redirecionamento(
        request=request, prox=prox if prox else request.url_for("site-nota").path
    )
    dados = {
        "request": request,
        "usuario_atual": usuario_atual,
        "telegram_bot_nome": config.TELEGRAM_BOT_NOME,
        "prox": prox,
    }
    return templates.TemplateResponse(name="usuario/entrar.html", context=dados)


@rota.get("/sair/", response_class=RedirectResponse, name="site-usuario-sair")
def sair(request: Request) -> RedirectResponse:
    """
    Encerra o processo de autenticação de um usuário.
    """
    resposta = RedirectResponse(url=request.url_for("site-index"))
    resposta.delete_cookie(key="usuario_atual")
    return resposta


@rota.get("/cadastrar/", response_class=HTMLResponse, name="site-usuario-cadastrar")
def cadastrar(
    request: Request,
    usuario_atual: md_usuario.Usuario = Depends(usuario_atual_site),
    prox: str = None,
) -> HTMLResponse:
    """
    Página para criação de um usuário.
    """
    if usuario_atual:
        return RedirectResponse(url=request.url_for("site-index"))
    prox = sq.validar_redirecionamento(
        request=request, prox=prox if prox else request.url_for("site-nota").path
    )
    dados = {
        "request": request,
        "usuario_atual": usuario_atual,
        "regex_apelido": config.REGEX_APELIDO,
        "regex_senha": config.REGEX_SENHA,
        "prox": prox,
    }
    return templates.TemplateResponse(name="usuario/cadastrar.html", context=dados)
