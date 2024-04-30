from fastapi import APIRouter, Request, Response, Depends
from fastapi.responses import RedirectResponse

from utils import seguranca as sq
from dependencias import usuario_atual_api
from apps.usuario import esquemas as eq
from apps.usuario import repositorios as rp


rota = APIRouter(prefix="/usuario", tags=["Usuário"])


@rota.post("/", response_model=eq.AutenticarRetorno, name="api-usuario-criar")
def criar(response: Response, novo_usuario: eq.NovoUsuario) -> eq.AutenticarRetorno:
    """
    Inicia o processo de criação de um novo usuário no sistema.

    Args:
        novo_usuario (eq.NovoUsuario): O novo usuário a ser criado.

    Returns:
        eq.AutenticarRetorno: O token de autenticação.
    """
    resposta = rp.criar_usuario(novo_usuario)
    response.set_cookie(
        key="usuario_atual",
        value=resposta.token,
        max_age=sq.expiracao_cookie_usuario_atual(),
    )
    return resposta


@rota.put("/editar-senha/", response_model=None, name="api-usuario-editar-senha")
def editar_senha(
    editar_senha: eq.EditarSenha, usuario_atual: eq.Usuario = Depends(usuario_atual_api)
) -> None:
    """
    Edita a senha do usuário atual.

    Args:
        editar_senha (eq.EditarSenha): Dados para a edição da senha.
        usuario_atual (eq.Usuário): O usuário que vai editar a senha.

    Returns:
        None
    """
    return rp.editar_senha(editar_senha=editar_senha, usuario_atual=usuario_atual)


@rota.put(
    "/vincular-telegram/", response_model=None, name="api-usuario-vincular-telegram"
)
def vincular_telegram(
    *,
    usuario_atual: eq.Usuario = Depends(usuario_atual_api),
    autenticar_telegram: eq.AutenticarTelegramRequisicao,
) -> None:
    """
    Vincula uma conta Telegram ao usuário atual.

    Args:
        autenticar_telegram (eq.AutenticarTelegramRequisicao): As credenciais da conta Telegram.
        usuario_atual (eq.Usuário): O usuário.

    Returns:
        None
    """
    return rp.vincular_telegram(
        usuario_atual=usuario_atual, autenticar_telegram=autenticar_telegram
    )


@rota.delete(
    "/desvincular-telegram/",
    response_model=None,
    name="api-usuario-desvincular-telegram",
)
def desvincular_telegram(
    usuario_atual: eq.Usuario = Depends(usuario_atual_api),
) -> None:
    """
    Remove a vinculação do usuário atual com uma conta Telegram.

    Args:
        usuario_atual (eq.Usuário): O usuário atual.

    Returns:
        None
    """
    return rp.desvincular_telegram(usuario_atual=usuario_atual)


@rota.post(
    "/autenticar",
    response_model=eq.AutenticarRetorno,
    name="api-usuario-autenticar",
)
def autenticar(
    response: Response, autenticar_req: eq.AutenticarRequisicao
) -> eq.AutenticarRetorno:
    """
    Inicia o processo de autenticação de um usuário.

    Args:
        autenticar_req (eq.AutenticarRequisicao): As credenciais do usuário.

    Returns:
        eq.AutenticarRetorno: O token de autenticação.
    """
    resposta = rp.autenticar(autenticar_req)
    response.set_cookie(
        key="usuario_atual",
        value=resposta.token,
        max_age=sq.expiracao_cookie_usuario_atual(),
    )
    return resposta


@rota.post(
    "/autenticar-telegram/",
    response_model=eq.AutenticarRetorno,
    name="api-usuario-autenticar-telegram",
)
def autenticar_telegram(
    request: Request,
    response: Response,
    autenticar_telegram: eq.AutenticarTelegramRequisicao,
    prox: str = None,
) -> eq.AutenticarRetorno | RedirectResponse:
    """
    Inicia o processo de autenticação de um usuário pelo telegram.

    Args:
        autenticar_telegram (eq.AutenticarTelegramRequisicao): As credenciais do usuário.

    Returns:
        eq.AutenticarRetorno: O token de autenticação.
        RedirectResponse: Redireciona o usuário para a proxima rota.
    """
    resposta = rp.autenticar_telegram(autenticar_telegram)
    cookie = dict(
        key="usuario_atual",
        value=resposta.token,
        max_age=sq.expiracao_cookie_usuario_atual(),
    )
    if not prox:
        response.set_cookie(**cookie)
        return resposta
    else:
        prox = sq.validar_redirecionamento(request=request, prox=prox)
        redirect = RedirectResponse(url=prox)
        redirect.set_cookie(**cookie)
        return redirect
