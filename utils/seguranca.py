import re
import hmac
import hashlib
from datetime import datetime, timedelta

import bcrypt
from jose import JWTError, jwt
from fastapi import Request

import config
from apps.usuario import esquemas as eq_usuario


def gerar_hash(senha: str) -> str:
    """
    Gera um hash para a senha informada.

    Args:
        senha (str): A senha a ser hasheada.

    Returns:
        str: O hash da senha informada.
    """
    senha_bytes = senha.encode("utf-8")
    salt = bcrypt.gensalt()
    senha_hashed = bcrypt.hashpw(password=senha_bytes, salt=salt)
    return senha_hashed.decode("utf-8")


def checar_senha(senha: str, senha_hashed: str) -> bool:
    """
    Verifica se a senha informada corresponde ao hash informado.

    Args:
        senha (str): A senha a ser verificada.
        senha_hashed (str): O hash da senha informada.

    Returns:
        bool: True se a senha corresponder ao hash, False caso contrário.
    """
    senha_bytes = senha.encode("utf-8")
    senha_hashed_bytes = senha_hashed.encode("utf-8")
    return bcrypt.checkpw(password=senha_bytes, hashed_password=senha_hashed_bytes)


def gerar_token_jwt(dados: eq_usuario.JWTInfo) -> str:
    """
    Gera um token jwt de acesso para o usuário.

    Args:
        dados (eq_usuario.JWTInfo): Os dados do usuário.

    Returns:
        str: O token jwt de acesso.
    """
    dados_copia = dados.model_dump()
    jwt_codificado = jwt.encode(claims=dados_copia, key=config.JWT_CHAVE_SECRETA)
    return jwt_codificado


def decodificar_token_jwt(token: str) -> eq_usuario.JWTInfo | None:
    """
    Decodifica o token.

    Args:
        token (str): O token jwt a ser decodificado.

    Returns:
        eq_usuario.JWTInfo | None: Os dados do usuário ou None caso o token seja inválido.
    """
    try:
        dados = jwt.decode(token=token, key=config.JWT_CHAVE_SECRETA)
        return eq_usuario.JWTInfo(**dados)
    except JWTError:
        return None


def expiracao_cookie_usuario_atual() -> int:
    """
    Retorna os segundos de expiração do cookie do usuário atual.

    Returns:
        int: Os segundos de expiração do cookie do usuário atual.
    """
    return config.JWT_EXPIRACAO_ACESSO_MINUTOS * 60


def validar_redirecionamento(request: Request, prox: str) -> str:
    """
    Valida se o caminho para onde o usuário será redirecionado é válido
    e seguro.

    Args:
        request (Request): A requisição HTTP.
        prox (str): O caminho para onde o usuário será redirecionado.

    Returns:
        str: O caminho seguro para onde o usuário será redirecionado.
    """
    if prox is None:
        prox = request.url_for("site-index").path
    else:
        regex = re.compile(r"^\/{1}[\/\w\?\&\=]+[\/\w_\-]*$")
        prox_valido = re.match(regex, prox) is not None
        if not prox_valido:
            prox = request.url_for("site-index")
    return prox


def validar_dados_telegram(
    autenticar_telegram: eq_usuario.AutenticarTelegramRequisicao,
) -> bool:
    """
    Valida os dados do Telegram.

    Args:
        autenticar_telegram (eq_usuario.AutenticarTelegramRequisicao): Os dados do telegram.

    Returns:
        bool: True se os dados foram validos e False caso contrário.
    """
    token_bot = config.TELEGRAM_BOT_TOKEN
    try:
        chave_secreta = hashlib.sha256(token_bot.encode()).digest()
        dados = dict(
            auth_date=autenticar_telegram.auth_date,
            first_name=autenticar_telegram.first_name,
            hash=autenticar_telegram.hash,
            id=autenticar_telegram.id,
            last_name=autenticar_telegram.last_name,
            photo_url=autenticar_telegram.photo_url,
            username=autenticar_telegram.username,
        )
        hash_origem = dados.get("hash")
        dados.pop("hash")

        _ = [f"{c}={v}" if v else None for c, v in dados.items()]
        _ = list(filter(None, _))
        mensagem = "\n".join(_)
        hash_mensagem = hmac.new(
            key=chave_secreta, msg=mensagem.encode(), digestmod=hashlib.sha256
        ).hexdigest()
        hashs_iguais = hmac.compare_digest(hash_mensagem, hash_origem)
        expiracao_valida = (
            datetime.fromtimestamp(autenticar_telegram.auth_date)
            + timedelta(minutes=config.JWT_EXPIRACAO_ACESSO_MINUTOS)
            > datetime.now()
        )
        if hashs_iguais and expiracao_valida:
            return True
        return False
    except Exception:
        return False
