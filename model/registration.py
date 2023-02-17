from typing import Dict, List, Protocol
from datetime import time
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from .base import ManagedEntity


class Registration(ManagedEntity):
    __tablename__ : str = "registration"
    __status : Mapped[str] = mapped_column("str")
    __student_id : Mapped[int] = \
        mapped_column("student_id", ForeignKey('student.id'))
    __course_section_id : Mapped[int] = \
        mapped_column("course_section_id", ForeignKey('course_section.id'))


    def __init__(self, id : int, status : str) -> None:
        super().__init__(id)
        self.__status : str = status

    @property
    def status(self) -> str:
        return self.status

    @status.setter
    def status(self, s : str) -> None:
        self.__status = s

    def counts_towards_cap(self) -> bool:
        return self.status == "registered"
