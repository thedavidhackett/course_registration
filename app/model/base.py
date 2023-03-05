from typing import Dict, Optional, Protocol

from sqlalchemy.orm import declared_attr, DeclarativeBase

class Base(DeclarativeBase):
    pass

class ManagedEntity(Base):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> Optional[str]:
        name : str = cls.__name__[0].lower()
        for char in cls.__name__[1:]:
            if (char.isupper()):
                name += "_"
            name += char.lower()

        return name

class Viewable(Protocol):
    def view(self) -> Dict[str, object]:
        pass
