from fastapi import APIRouter, Depends
from apps.nota import repositorios as rp

from dependencias import usuario_atual_api
from apps.nota import esquemas as eq
from apps.usuario import esquemas as eq_usuario


rota = APIRouter(prefix="/nota", tags=["Nota"])


@rota.get("/", response_model=eq.ResultadoPesquisa, name="api-nota")
def obter_notas(
    usuario_atual: eq_usuario.Usuario = Depends(usuario_atual_api),
    filtro: eq.FiltroPesquisa = Depends(),
) -> eq.ResultadoPesquisa:
    """
    Retorna todas as notas do usuário.

    Returns:
        eq.ResultadoPesquisa: As notas do usuário.
    """
    return rp.obter_notas(usuario_atual=usuario_atual, filtro=filtro)


@rota.get("/{id}/", response_model=eq.Nota, name="api-nota-id")
def obter_nota(
    id: int,
    usuario_atual: eq_usuario.Usuario = Depends(usuario_atual_api),
) -> eq.Nota:
    """
    Retorna uma nota.

    Args:
        id (int): O id da nota.
        usuario_atual (eq.Usuário): O usuário.

    Returns:
        eq.Nota: A nota.
    """
    return rp.obter_nota(id=id, usuario_atual=usuario_atual)


@rota.put("/{id}/", response_model=eq.Nota, name="api-nota-editar")
def editar_nota(
    id: int,
    editar_nota: eq.EditarNota,
    usuario_atual: eq_usuario.Usuario = Depends(usuario_atual_api),
) -> eq.Nota:
    """
    Edita uma nota.

    Args:
        id (int): O id da nota.
        editar_nota (eq.EditarNota): A edição da nota.
        usuario_atual (eq.Usuário): O usuário.

    Returns:
        eq.Nota: A nota editada.
    """
    return rp.editar_nota(id=id, editar_nota=editar_nota, usuario_atual=usuario_atual)


@rota.post("/", response_model=eq.Nota, name="api-nota-criar")
def criar_nota(
    nova_nota: eq.NovaNota,
    usuario_atual: eq_usuario.Usuario = Depends(usuario_atual_api),
) -> eq.Nota:
    """
    Cria uma nova nota.

    Args:
        nova_nota (eq.NovaNota): A nova nota.
        usuario_atual (eq.Usuário): O usuário.

    Returns:
        eq.Nota: Anota criada.
    """
    return rp.criar_nota(nova_nota=nova_nota, usuario_atual=usuario_atual)


@rota.delete("/{id}/", response_model=eq.Nota, name="api-nota-deletar")
def deletar_nota(
    id: int,
    usuario_atual: eq_usuario.Usuario = Depends(usuario_atual_api),
) -> eq.Nota:
    """
    Deleta uma nota.

    Args:
        id (int): O id da nota.
        usuario_atual (eq.Usuário): O usuário.

    Returns:
        eq.Nota: A nota deletada.
    """
    return rp.deletar_nota(id=id, usuario_atual=usuario_atual)
