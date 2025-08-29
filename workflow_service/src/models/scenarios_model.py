from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger


class ScenariosModel(Base):
    __tablename__ = "scenarios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, nullable=True, default=None)
    owner_email: Mapped[str] = mapped_column(nullable=False, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    # event: Mapped[dict] = mapped_column(
    #     JSON,
    #     nullable=False,
    #     doc="JSON structure: { 'type': str, 'source': str }"
    # )
    # conditions: Mapped[dict] = mapped_column(
    #     JSON,
    #     nullable=False,
    #     doc="JSON structure: { 'type': str, 'params': dict }"
    # )
    # actions: Mapped[dict] = mapped_column(
    #     JSON,
    #     nullable=False,
    #     doc="JSON structure: { 'type': str, 'params': dict }"
    # )


class EventsModel(Base):
    __tablename__ = "events"


class ConditionsModel(Base):
    __tablename__ = "conditions"


class ActionsModel(Base):
    __tablename__ = "actions"
