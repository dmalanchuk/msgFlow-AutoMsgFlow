from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from src.models.login_tokens_model import LoginTokens


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(unique=True,nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    tokens: Mapped[list["LoginTokens"]] = relationship(back_populates="user")