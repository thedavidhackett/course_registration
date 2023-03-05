from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import ManagedEntity

class Registration(ManagedEntity):
    __id : Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)
    __status : Mapped[str] = mapped_column("status", String(20))
    student_id : Mapped[int] = \
        mapped_column("student_id", ForeignKey('student.id'))
    course_section_id : Mapped[int] = \
        mapped_column("course_section_id", ForeignKey('course_section.id'))


    def __init__(self, status : str, student_id : int, course_section_id : int) -> None:
        super().__init__()
        self.__status : str = status
        self.student_id : int = student_id
        self.course_section_id : int = course_section_id

    @property
    def id(self) -> int:
        return self.__id

    @property
    def status(self) -> str:
        return self.__status

    @status.setter
    def status(self, s : str) -> None:
        self.__status = s

    def counts_towards_cap(self) -> bool:
        return self.status == "registered"
