from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class ScenariosModel(Base):
    __tablename__ = "scenarios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

