from typing import Dict, Protocol
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

Base = declarative_base()

class ManagedEntity(Base):
    __abstract__ = True
    __id : Mapped[int] = mapped_column("id", primary_key=True)

    def __init__(self, id : int) -> None:
        self.__id : int = id

    @declared_attr.directive
    def __tablename__(cls) -> str:
        name : str = cls.__name__[0].lower()
        for char in cls.__name__[1:]:
            if (char.isupper()):
                name += "_"
            name += char.lower()

        return name

    @property
    def id(self) -> int:
        return self.__id



class Viewable(Protocol):
    def view() -> Dict[str, object]:
        pass
