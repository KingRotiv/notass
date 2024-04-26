from fastapi import APIRouter, Response, Depends

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
