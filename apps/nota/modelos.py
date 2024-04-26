from datetime import datetime

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db import Base


class Nota(Base):
    __tablename__ = "nota"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuario.id"))
    titulo: Mapped[str] = mapped_column(String(50))
    texto: Mapped[str] = mapped_column(String(4000))
    data_registro: Mapped[datetime] = mapped_column(default=datetime.now)
    data_alteracao: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )
