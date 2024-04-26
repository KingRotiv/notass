from fastapi import Depends, Cookie, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.exception_handlers import HTTPException

from utils import seguranca as sq
from apps.usuario import repositorios as rp_usuario
from apps.usuario import esquemas as eq_usuario


auth_bearer = HTTPBearer(auto_error=False)


def _usuario_atual(
    usuario_atual, credencial, omitir_erro: bool = False
) -> eq_usuario.Usuario | None:
    """
    Retorna o usuário atual ou None/Exception se o usuário não for válido.
    """
    if usuario_atual or credencial:
        if credencial:
            token = credencial.credentials
        else:
            token = usuario_atual
        dados = sq.decodificar_token_jwt(token=token)
        if dados is not None:
            usuario = eq_usuario.Usuario.model_validate(
                obj=rp_usuario.obter_usuario(dados=dados), from_attributes=True
            )
            return usuario
    if omitir_erro:
        return None
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Credenciais inválidas."
        )


def usuario_atual_api(
    usuario_atual: str | None = Cookie(default=None, include_in_schema=False),
    credencial: HTTPAuthorizationCredentials | None = Depends(auth_bearer),
):
    return _usuario_atual(usuario_atual=usuario_atual, credencial=credencial)


def usuario_atual_site(
    usuario_atual: str | None = Cookie(default=None, include_in_schema=False),
    credencial: HTTPAuthorizationCredentials | None = Depends(auth_bearer),
):
    return _usuario_atual(
        omitir_erro=True, usuario_atual=usuario_atual, credencial=credencial
    )
