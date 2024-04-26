from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class Usuario(Base):
    """
    Modelo da tabela de usuário.
    """

    __tablename__ = "usuario"

    id: Mapped[int] = mapped_column(primary_key=True)
    apelido: Mapped[str] = mapped_column(String(20), unique=True)
    senha_hashed: Mapped[str] = mapped_column(String(60))
    data_registro: Mapped[datetime] = mapped_column(default=datetime.now)
    notas: Mapped[list["Nota"]] = relationship(backref="nota")
