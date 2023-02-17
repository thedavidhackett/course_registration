from typing import Optional, Type
from model.base import ManagedEntity
from sqlalchemy.orm import Session


class EntityManager:
    def __init__(self, db) -> None:
        self.__db = db

    def get_by_id(self, Cls : Type[ManagedEntity], id : int) -> Optional[ManagedEntity]:
        obj : Optional[ManagedEntity]
        with Session(self.__db) as s:
            obj = s.get(Cls, id)

        return obj
