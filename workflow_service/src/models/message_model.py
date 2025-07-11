from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, ForeignKey


class MessageModel(Base):
    __tablename__ = "incoming_messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("scenarios.chat_id"), nullable=True, default=None)
    text: Mapped[str] = mapped_column(nullable=False)
