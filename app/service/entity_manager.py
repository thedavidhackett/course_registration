from typing import Optional, Type, List
from model.base import ManagedEntity
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import Select


class EntityManager:
    def __init__(self, db) -> None:
        self.__db = db

    def get_by_id(self, Cls : Type[ManagedEntity], id : int) -> Optional[ManagedEntity]:
        obj : Optional[ManagedEntity]
        with Session(self.__db) as s:
            obj = s.get(Cls, id)

        return obj

    def add(self, obj : ManagedEntity) -> None:
        with Session(self.__db) as s:
            s.add(obj)
            s.commit()

    def get_by_criteria(self, statement : Select) -> List[ManagedEntity]:
        result : List[ManagedEntity]
        with Session(self.__db) as s:
            result = [obj for obj in s.scalars(statement)]

        return result


    def get_one_by_criteria(self, statement : Select) -> Optional[ManagedEntity]:
        obj : Optional[ManagedEntity]
        with Session(self.__db) as s:
            obj = s.scalars(statement).one()

        return obj
