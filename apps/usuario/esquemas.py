from datetime import datetime, timedelta
from typing import Annotated

from typing_extensions import Self
from pydantic import BaseModel, ConfigDict, SecretStr, constr, model_validator

import config
from utils import seguranca as sq


class EditarSenha(BaseModel):
    """
    Esquema de dados para edição de uma senha.

    Attributtes:
        senha (str): A senha do usuário.
        nova_senha (str): A nova senha do usuário.
        _nova_senha_hashed (str) (read-only): O hash da nova senha.
    """

    senha: Annotated[
        SecretStr,
        constr(to_lower=True, strip_whitespace=True, pattern=config.REGEX_SENHA),
    ]
    nova_senha: Annotated[
        SecretStr,
        constr(to_lower=True, strip_whitespace=True, pattern=config.REGEX_SENHA),
    ]
    _nova_senha_hashed: str

    @model_validator(mode="after")
    def validar_modelo(self) -> Self:
        self._nova_senha_hashed = sq.gerar_hash(self.nova_senha.get_secret_value())
        return self


class NovoUsuario(BaseModel):
    """
    Esquema de dados para criação de um novo usuário.

    Attributtes:
        apelido (str): O apelido do novo usuário.
        senha (str): A senha do novo usuário.
        _senha_hashed (str) (read-only): O hash da senha.
    """

    apelido: constr(
        to_lower=True, strip_whitespace=True, pattern=config.REGEX_APELIDO
    )  # type: ignore
    senha: Annotated[
        SecretStr,
        constr(to_lower=True, strip_whitespace=True, pattern=config.REGEX_SENHA),
    ]
    _senha_hashed: str

    @model_validator(mode="after")
    def validar_modelo(self) -> Self:
        self._senha_hashed = sq.gerar_hash(self.senha.get_secret_value())
        return self


class Usuario(BaseModel):
    """
    Esquema de dados de um usuário.

    Attributtes:
        id (int): O id do usuário.
        apelido (str): O apelido do usuário.
        data_registro (datetime): A data de registro do usuário.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    apelido: str
    id_telegram: int | None
    data_registro: datetime


class AutenticarRequisicao(NovoUsuario):
    """
    Esquema de dados para autenticação de um usuário.

    Attributtes:
        apelido (str): O apelido do usuário.
        senha (str): A senha do usuário.
    """


class AutenticarRetorno(BaseModel):
    """
    Esquema de dados para retorno de autenticação de um usuário.

    Attributtes:
        token (str): O token de autenticação.
    """

    token: str


class JWTInfo(BaseModel):
    """
    Esquema de dados armazenados no token jwt.

    Attributtes:
        exp (datetime | None): A data de expiração do token.
        apelido (str): O apelido do usuário.
        id (int): O id do usuário.
    """

    exp: datetime | None = None
    apelido: str
    id: int

    @model_validator(mode="after")
    def validar_modelo(self) -> Self:
        if self.exp is None:
            self.exp = datetime.utcnow() + timedelta(
                minutes=config.JWT_EXPIRACAO_ACESSO_MINUTOS
            )
        return self


class AutenticarTelegramRequisicao(BaseModel):
    """
    Esquema de dados para autenticação de um usuário pelo telegram.

    Attributtes:
        id (int): O id do telegram.
        first_name (str): O primeiro nome do usuário no telegram.
        last_name (str): O sobrenome do usuário no telegram.
        username (str): O nome de usuário no telegram.
        photo_url (str): A imagem de perfil do usuário no telegram.
        auth_date (int): A data de autenticação do usuário no telegram.
        hash (str): O hash da autenticação do usuário no telegram.
    """

    id: int
    first_name: str = ""
    last_name: str = ""
    username: str = ""
    photo_url: str = ""
    auth_date: int
    hash: str
