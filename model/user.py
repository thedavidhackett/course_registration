from abc import ABC, abstractmethod
from typing import Dict, List
from datetime import time
from .base import ManagedEntity
from sqlalchemy import ForeignKey
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .registration import Registration

class User(ManagedEntity):
    __abstract__ = True
    __first_name : Mapped[str] = mapped_column("first_name")
    __last_name : Mapped[str] = mapped_column("last_name")
    __password : Mapped[str] = mapped_column("password")

    def __init__(self, id : int, first_name: str, last_name : str) -> None:
        super().__init__(id)
        self.__first_name : str = first_name
        self.__last_name : str = last_name
        self.__password : str = ""

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
    __level : Mapped[str] = mapped_column("level")
    __registrations : Mapped[List[Registration]] = relationship(lazy="subquery")

    def __init__(self, id: int, first_name: str, last_name: str, level : str) -> None:
        super().__init__(id, first_name, last_name)
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
