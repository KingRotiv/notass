from sqlalchemy import select
from loguru import logger
from fastapi import status
from fastapi.exceptions import HTTPException

from db import session
from apps.nota import modelos as md
from apps.nota import esquemas as eq
from apps.usuario import esquemas as eq_usuario


def obter_notas(
    usuario_atual: eq_usuario.Usuario, filtro: eq.FiltroPesquisa
) -> eq.ResultadoPesquisa:
    """
    Retorna as notas do usuário.

    Args:
        usuario_atual (eq.Usuário): O usuário.

    Returns:
        eq.ResultadoPesquisa: Resultado da pesquisa.
    """
    logger.info(f"Obtendo notas do usuário {usuario_atual.apelido}")
    with session() as s:
        q = (
            select(md.Nota)
            .where(md.Nota.id_usuario == usuario_atual.id)
            .order_by(
                (
                    md.Nota.data_alteracao.desc()
                    if filtro.ordem == eq.FiltroPesquisaOrdem.data_alteracao
                    else md.Nota.data_registro.desc()
                ),
                md.Nota.id,
            )
        )
        r = s.execute(q).scalars().all()
        resultados = [eq.Nota.model_validate(nota) for nota in r]
        return eq.ResultadoPesquisa(resultados=resultados)


def obter_nota(id: int, usuario_atual: eq_usuario.Usuario) -> md.Nota:
    """
    Retorna uma nota.

    Args:
        id (int): O id da nota.
        usuario_atual (eq.Usuário): O usuário.

    Raises:
        HTTPException: Se a nota não existir.

    Returns:
        eq.Nota: A nota.
    """
    with session() as s:
        q = select(md.Nota).where(
            md.Nota.id == id and md.Nota.id_usuario == usuario_atual.id
        )
        r = s.execute(q).scalar()
        if r:
            logger.info(f"Obtendo nota {id} do usuário {usuario_atual.apelido}")
            return r
        logger.info(f"Nota {id} do usuário {usuario_atual.apelido} não encontrada")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Nota não encontrada."
        )


def editar_nota(
    id: int, editar_nota: eq.EditarNota, usuario_atual: eq_usuario.Usuario
) -> md.Nota:
    """
    Edita uma nota.

    Args:
        id (int): O id da nota.
        editar_nota (eq.EditarNota): A edição da nota.
        usuario_atual (eq.Usuário): O usuário.

    Raises:
        HTTPException: Se a nota não existir.

    Returns:
        md.Nota: A nota editada.
    """
    nota = obter_nota(id=id, usuario_atual=usuario_atual)
    with session() as s:
        try:
            nota = s.merge(nota)
            for k, v in editar_nota.model_dump().items():
                setattr(nota, k, v)
            s.commit()
            s.refresh(nota)
            logger.info(f"Nota {id} do usuário {usuario_atual.apelido} editada")
            return nota
        except Exception as ex:
            s.rollback()
            logger.exception(ex)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def criar_nota(nova_nota: eq.NovaNota, usuario_atual: eq_usuario.Usuario) -> md.Nota:
    """
    Cria uma nova nota.

    Args:
        nova_nota (eq.NovaNota): A nova nota.
        usuario_atual (eq.Usuário): O usuário.

    Returns:
        md.Nota: A nova nota criada.
    """
    with session() as s:
        try:
            nota = md.Nota(
                id_usuario=usuario_atual.id,
                **nova_nota.model_dump(),
            )
            s.add(nota)
            s.commit()
            s.refresh(nota)
            logger.info(f"Nota {nota.id} do usuário {usuario_atual.apelido} criada")
            return nota
        except Exception as ex:
            s.rollback()
            logger.exception(ex)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def deletar_nota(id: int, usuario_atual: eq_usuario.Usuario) -> md.Nota:
    """
    Deleta uma nota.

    Args:
        id (int): O id da nota.
        usuario_atual (eq.Usuário): O usuário.

    Raises:
        HTTPException: Se a nota não existir.

    Returns:
        md.Nota: A nota deletada.
    """
    nota = obter_nota(id=id, usuario_atual=usuario_atual)
    with session() as s:
        nota = s.merge(nota)
        try:
            s.delete(nota)
            s.commit()
            logger.info(f"Nota {id} do usuário {usuario_atual.apelido} deletada")
            return nota
        except Exception as ex:
            s.rollback()
            logger.exception(ex)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
