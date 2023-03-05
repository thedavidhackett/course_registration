from abc import ABC, abstractmethod
from typing import Optional, Type, List

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import Select

from model.base import ManagedEntity



class EntityManagerInterface(ABC):
    @abstractmethod
    def get_by_id(self, Cls : Type[ManagedEntity], id : int) -> Optional[ManagedEntity]:
        pass

    @abstractmethod
    def add(self, obj : ManagedEntity) -> None:
        pass

    @abstractmethod
    def get_by_criteria(self, statement : Select) -> List[ManagedEntity]:
        pass

    @abstractmethod
    def get_one_by_criteria(self, statement : Select) -> Optional[ManagedEntity]:
        pass

    @abstractmethod
    def delete(self, obj : ManagedEntity) -> None:
        pass

class EntityManager(EntityManagerInterface):
    def __init__(self, db) -> None:
        self.__db = Session(db)

    def get_by_id(self, Cls : Type[ManagedEntity], id : int) -> Optional[ManagedEntity]:
        obj : Optional[ManagedEntity] = self.__db.get(Cls, id)
        return obj

    def add(self, obj : ManagedEntity) -> None:
        self.__db.add(obj)
        self.__db.commit()

    def get_by_criteria(self, statement : Select) -> List[ManagedEntity]:
        result : List[ManagedEntity] = [obj for obj in self.__db.scalars(statement)]

        return result

    def get_one_by_criteria(self, statement : Select) -> Optional[ManagedEntity]:
        obj : Optional[ManagedEntity] = self.__db.scalars(statement).one_or_none()

        return obj

    def delete(self, obj : ManagedEntity) -> None:
        self.__db.delete(obj)
        self.__db.commit()
