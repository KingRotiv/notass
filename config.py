from decouple import config


# Geral
NOME_APP = "Notass"

# Telegram bot
TELEGRAM_BOT_TOKEN = config("TELEGRAM_BOT_TOKEN")
TELEGRAM_BOT_NOME = config("TELEGRAM_BOT_NOME")
TELEGRAM_BOT_URL = f"https://t.me/{TELEGRAM_BOT_NOME}"

# Segurança
JWT_EXPIRACAO_ACESSO_MINUTOS = config("JWT_EXPIRACAO_ACESSO_MINUTOS", cast=int)
JWT_CHAVE_SECRETA = config("JWT_CHAVE_SECRETA")

# Regex
REGEX_APELIDO = "^[a-zA-Z0-9]{5,20}$"
REGEX_SENHA = "^(?=.{8,30})(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?!.*\s).*$"
