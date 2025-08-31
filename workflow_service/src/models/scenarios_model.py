from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB


class ScenariosModel(Base):
    __tablename__ = "scenarios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, nullable=True, default=None)
    owner_email: Mapped[str] = mapped_column(nullable=False, index=True)
    name: Mapped[str] = mapped_column(nullable=False)

    events: Mapped[list["EventsModel"]] = relationship(
        back_populates="scenario", cascade="all, delete-orphan"
    )
    conditions: Mapped[list["ConditionsModel"]] = relationship(
        back_populates="scenario", cascade="all, delete-orphan"
    )
    actions: Mapped[list["ActionsModel"]] = relationship(
        back_populates="scenario", cascade="all, delete-orphan"
    )

    __table_args__ = (UniqueConstraint("owner_email", "name", name="_chat_owner_uc"),)


class EventsModel(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    scenario_id: Mapped[int] = mapped_column(ForeignKey("scenarios.id", ondelete="CASCADE"))
    type: Mapped[str] = mapped_column(nullable=False)
    source: Mapped[str] = mapped_column(nullable=False)

    scenario: Mapped["ScenariosModel"] = relationship(back_populates="events")


class ConditionsModel(Base):
    __tablename__ = "conditions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    scenario_id: Mapped[int] = mapped_column(ForeignKey("scenarios.id", ondelete="CASCADE"))
    type: Mapped[str] = mapped_column(nullable=False)
    params: Mapped[dict] = mapped_column(JSONB, nullable=False)

    scenario: Mapped["ScenariosModel"] = relationship(back_populates="conditions")


class ActionsModel(Base):
    __tablename__ = "actions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    scenario_id: Mapped[int] = mapped_column(ForeignKey("scenarios.id", ondelete="CASCADE"))
    type: Mapped[str] = mapped_column(nullable=False)
    params: Mapped[dict] = mapped_column(JSONB, nullable=False)

    scenario: Mapped["ScenariosModel"] = relationship(back_populates="actions")
