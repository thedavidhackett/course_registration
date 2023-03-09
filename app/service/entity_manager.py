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
    def get_all(self, Cls : Type[ManagedEntity]) -> List[ManagedEntity]:
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
        self.__db = db

    def get_by_id(self, Cls : Type[ManagedEntity], id : int) -> Optional[ManagedEntity]:
        with Session(self.__db) as s:
            obj : Optional[ManagedEntity] = s.get(Cls, id)
            return obj

    def get_all(self, Cls: Type[ManagedEntity]) -> List[ManagedEntity]:
        with Session(self.__db) as s:
            obj : ManagedEntity
            return [obj for obj in s.query(Cls).all()]

    def add(self, obj : ManagedEntity) -> None:
        with Session(self.__db) as s:
            s.add(obj)
            s.commit()

    def get_by_criteria(self, statement : Select) -> List[ManagedEntity]:
        with Session(self.__db) as s:
            result : List[ManagedEntity] = [obj for obj in s.scalars(statement)]

            return result

    def get_one_by_criteria(self, statement : Select) -> Optional[ManagedEntity]:
        with Session(self.__db) as s:
            obj : Optional[ManagedEntity] = s.scalars(statement).one_or_none()

            return obj

    def delete(self, obj : ManagedEntity) -> None:
        with Session(self.__db) as s:
            s.delete(obj)
            s.commit()
