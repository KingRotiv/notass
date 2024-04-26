from sqlalchemy import select
from fastapi import status
from fastapi.exceptions import HTTPException

from db import session
from utils import seguranca as sq
from apps.usuario import esquemas as eq
from apps.usuario import modelos as md


def criar_usuario(novo_usuario: eq.NovoUsuario) -> eq.AutenticarRetorno:
    """
    Cria um novo usuário no sistema.

    Args:
        novo_usuario (eq.NovoUsuario): O novo usuário a ser criado.

    Raises:
        HTTPException: Se o usuário já existir.
        HTTPException: Se ocorrer um erro interno no servidor.

    Returns:
        eq.AutenticarRetorno: O token de autenticação.
    """
    with session() as s:
        q_existe = select(md.Usuario).where(md.Usuario.apelido == novo_usuario.apelido)
        if s.execute(q_existe).scalar():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Usuário já existe."
            )
        try:
            usuario = md.Usuario(
                apelido=novo_usuario.apelido,
                senha_hashed=novo_usuario._senha_hashed,
            )
            s.add(usuario)
            s.commit()
            s.refresh(usuario)
            token = sq.gerar_token_jwt(
                dados=eq.JWTInfo(apelido=usuario.apelido, id=usuario.id)
            )
            return eq.AutenticarRetorno(token=token)
        except Exception:
            s.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def editar_senha(editar_senha: eq.EditarSenha, usuario_atual: eq.Usuario) -> None:
    """
    Edita a senha do usuário atual.

    Args:
        editar_senha (eq.EditarSenha): Dados para a edição da senha.
        usuario_atual (eq.Usuario): O usuário que vai editar a senha.

    Raises:
        HTTPException: Se as credenciais informadas forem inválidas.

    Returns:
        None
    """
    with session() as s:
        q = select(md.Usuario).where(md.Usuario.id == usuario_atual.id)
        usuario = s.execute(q).scalar()
        if not sq.checar_senha(
            senha=editar_senha.senha.get_secret_value(),
            senha_hashed=usuario.senha_hashed,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Senha atual inválida.",
            )
        try:
            usuario.senha_hashed = editar_senha._nova_senha_hashed
            s.commit()
            return None
        except Exception:
            s.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def obter_usuario(dados: eq.JWTInfo) -> md.Usuario:
    """
    Retorna o usuário pelo dados do token jwt.

    Args:
        dados (eq.JWTInfo): Os dados do usuário.

    Raises:
        HTTPException: Se o usuário não existir.

    Returns:
        md.Usuario: O usuário.
    """
    with session() as s:
        q = select(md.Usuario).where(
            md.Usuario.id == dados.id and md.Usuario.apelido == dados.apelido
        )
        r = s.execute(q).scalar()
        if r:
            return r
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado."
        )


def autenticar(autenticar: eq.AutenticarRequisicao) -> eq.AutenticarRetorno:
    """
    Autentica um usuário no sistema.

    Args:
        autenticar (eq.AutenticarRequisicao): As credenciais do usuário.

    Raises:
        HTTPException: Se as credenciais informadas forem inválidas.

    Returns:
        eq.AutenticarRetorno: O token de autenticação.
    """
    with session() as s:
        q = select(md.Usuario).where(md.Usuario.apelido == autenticar.apelido)
        usuario = s.execute(q).scalar()
        if usuario and sq.checar_senha(
            senha=autenticar.senha.get_secret_value(), senha_hashed=usuario.senha_hashed
        ):
            token = sq.gerar_token_jwt(
                dados=eq.JWTInfo(apelido=usuario.apelido, id=usuario.id)
            )
            return eq.AutenticarRetorno(token=token)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas."
        )
