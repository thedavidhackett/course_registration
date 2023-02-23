from abc import ABC, abstractmethod
from typing import Dict, List
from datetime import time
from .base import ManagedEntity
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import column_property


from .registration import Registration

class User(ManagedEntity):
    __abstract__ = True
    __id : Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)
    __first_name : Mapped[str] = mapped_column("first_name", String(100))
    __last_name : Mapped[str] = mapped_column("last_name", String(100))
    __password : Mapped[str] = mapped_column("password", String(100))

    def __init__(self, first_name: str, last_name : str) -> None:
        super().__init__()
        self.__first_name : str = first_name
        self.__last_name : str = last_name
        self.__password : str = ""

    @property
    def id(self) -> int:
        return self.__id

    @property
    def first_name(self) -> str:
        return self.__first_name

    @property
    def last_name(self) -> str:
        return self.__last_name

    @abstractmethod
    def full_name(self) -> str:
        pass

    @abstractmethod
    def view(self) -> Dict[str, object]:
        pass


class Student(User):
    __level : Mapped[str] = mapped_column("level", String(20))
    __registrations : Mapped[List[Registration]] = relationship(lazy="subquery")

    def __init__(self, first_name: str, last_name: str, level : str) -> None:
        super().__init__(first_name, last_name)
        self.__level = level
        self.__registrations : List[Registration] = []

    @property
    def level(self) -> str:
        return self.__level

    def full_name(self):
        return self.first_name + " " + self.last_name

    def view(self) -> Dict[str, object]:
        return {"id": self.id, "name": self.full_name(), "level" : self.level}

    def add_registration(self, r : Registration) -> None:
        self.__registrations.append(r)
