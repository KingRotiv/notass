from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, constr


class NovaNota(BaseModel):
    """
    Esquema de dados de uma nova nota.

    Attributtes:
        titulo (str): O título da nova nota.
        texto (str): O texto da nova nota.
    """

    titulo: constr(strip_whitespace=True, min_length=1, max_length=50)  # type: ignore
    texto: constr(strip_whitespace=True, min_length=1, max_length=4000)  # type: ignore


class EditarNota(NovaNota):
    """
    Esquema de dados de uma edição de uma nota.

    Attributtes:
        titulo (str): O novo título da nota.
        texto (str): O novo texto da nota.
    """


class Nota(BaseModel):
    """
    Esquema de dados de uma nota.

    Attributtes:
        id (int): O id da nota.
        id_usuario (int): O id do usuário.
        texto (str): O texto da nota.
        data_registro (datetime): A data de registro da nota.
        data_alteracao (datetime): A data de alteração da nota.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    id_usuario: int
    titulo: str
    texto: str
    data_registro: datetime
    data_alteracao: datetime


class FiltroPesquisaOrdem(str, Enum):
    data_alteracao = "Data de alteração"
    data_registro = "Data de registro"


class FiltroPesquisa(BaseModel):
    """
    Esquema de dados de um filtro de uma pesquisa.

    Attributtes:
        ordem (FiltroPesquisaOrdem): A ordem a ser mostrada na pesquisa.
    """

    ordem: FiltroPesquisaOrdem = FiltroPesquisaOrdem.data_alteracao


class ResultadoPesquisa(BaseModel):
    """
    Esquema de dados de um resultado de uma pesquisa.

    Attributtes:
        resultados (list[Nota]): Os resultados da pesquisa.
    """

    resultados: list[Nota]
