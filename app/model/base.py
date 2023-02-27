from typing import Dict, Protocol

from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ManagedEntity(Base):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        name : str = cls.__name__[0].lower()
        for char in cls.__name__[1:]:
            if (char.isupper()):
                name += "_"
            name += char.lower()

        return name

class Viewable(Protocol):
    def view(self) -> Dict[str, object]:
        pass
