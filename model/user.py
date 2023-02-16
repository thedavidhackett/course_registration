from abc import ABC, abstractmethod
from typing import Dict, List
from datetime import time
from .base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class User(Base):
    __abstract__ = True
    __id : Mapped[int] = mapped_column("id", primary_key=True)
    __first_name : Mapped[str] = mapped_column("first_name")
    __last_name : Mapped[str] = mapped_column("last_name")
    __password : Mapped[str] = mapped_column("password")

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    def __init__(self, id : int, first_name: str, last_name : str) -> None:
        self.__id : int = id
        self.__first_name : str = first_name
        self.__last_name : str = last_name
        self.__password : str = ""

    @property
    def id(self):
        return self.__id

    @property
    def first_name(self):
        return self.__first_name

    @property
    def last_name(self):
        return self.__last_name

    @abstractmethod
    def full_name(self):
        pass


class Student(User):
    __tablename__ : str = "student"
    __level : Mapped[str] = mapped_column("level")

    def __init__(self, id: int, first_name: str, last_name: str, level : str) -> None:
        super().__init__(id, first_name, last_name)
        self.__level = level

    @property
    def level(self) -> str:
        return self.__level

    def full_name(self):
        return self.first_name + " " + self.last_name

    def get_details(self) -> Dict[str, object]:
        return {"id": self.id, "name": self.full_name(), "level" : self.level}
