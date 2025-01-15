from sqlalchemy.orm import MappedColumn, mapped_column

from src.database import Base


class User(Base):
    __tablename__ = "user"

    id: MappedColumn[int] = mapped_column(primary_key=True)
    email: MappedColumn[str] = mapped_column(nullable=False)
    hashed_password: MappedColumn[str] = mapped_column(nullable=False)