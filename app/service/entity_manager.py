from abc import ABC, abstractmethod
from typing import Optional, Type, List, TypeVar, Tuple

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import Select

from model.base import ManagedEntity

T = TypeVar('T', bound=ManagedEntity)

class EntityManagerInterface(ABC):
    @abstractmethod
    def get_by_id(self, Cls : Type[T], id : int) -> Optional[T]:
        pass

    @abstractmethod
    def get_all(self, Cls : Type[T]) -> List[T]:
        pass

    @abstractmethod
    def add(self, obj : T) -> None:
        pass

    @abstractmethod
    def get_by_criteria(self, statement : Select[Tuple[T]]) -> List[T]:
        pass

    @abstractmethod
    def get_one_by_criteria(self, statement : Select[Tuple[T]]) -> Optional[T]:
        pass

    @abstractmethod
    def delete(self, obj : T) -> None:
        pass



class EntityManager(EntityManagerInterface):
    def __init__(self, db) -> None:
        self.__db = db

    def get_by_id(self, Cls : Type[T], id : int) -> Optional[T]:
        with Session(self.__db) as s:
            obj : Optional[T] = s.get(Cls, id)
            return obj

    def get_all(self, Cls: Type[T]) -> List[T]:
        with Session(self.__db) as s:
            obj : T
            return [obj for obj in s.query(Cls).all()]

    def add(self, obj : T) -> None:
        with Session(self.__db) as s:
            s.add(obj)
            s.commit()

    def get_by_criteria(self, statement : Select[Tuple[T]]) -> List[T]:
        with Session(self.__db) as s:
            result : List[T] = [obj for obj in s.scalars(statement)]

            return result

    def get_one_by_criteria(self, statement : Select[Tuple[T]]) -> Optional[T]:
        with Session(self.__db) as s:
            obj : Optional[T] = s.scalars(statement).one_or_none()

            return obj

    def delete(self, obj : T) -> None:
        with Session(self.__db) as s:
            s.delete(obj)
            s.commit()
