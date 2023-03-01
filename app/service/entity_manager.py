from typing import Optional, Type, List
from model.base import ManagedEntity
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import Select


class EntityManager:
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
        obj : Optional[ManagedEntity] = self.__db.scalars(statement).one()

        return obj
