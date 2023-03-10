from typing import Dict, List
from datetime import time

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import ManagedEntity
from .registration import Registration
from .user import Instructor, Professor

class Department(ManagedEntity):
    __id : Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)
    __name : Mapped[str] = mapped_column("name", String(100))
    __chair_id : Mapped[int] = mapped_column("chair_id", ForeignKey('professor.id'))
    _chair : Mapped[Professor] = relationship(lazy="subquery")

    def __init__(self, name : str, professor_id : int):
        super().__init__()
        self.__name : str = name
        self.__chair_id : int = professor_id

    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def chair_id(self) -> int:
        return self.__chair_id

    @property
    def chair(self) -> Professor:
        return self._chair

    def make_chair(self, professor : Professor):
        self.__chair_id = professor.id

    def view(self) -> Dict[str, object]:
        return {"id": self.id, "name": self.name}



class Course(ManagedEntity):
    __id : Mapped[int] = mapped_column("id", primary_key=True)
    __name : Mapped[str] = mapped_column("name", String(100))
    __description : Mapped[str] = mapped_column("description", String(255))
    __consent_required : Mapped[bool] = mapped_column("consent_required")
    __lab_required : Mapped[bool] = mapped_column("lab_required")
    __pre_reqs : Mapped[List["Course"]] = relationship(lazy="subquery")
    pre_req_for_id : Mapped[int] = mapped_column("pre_req_for_id", ForeignKey('course.id'), nullable=True)
    course_sections: Mapped[List["CourseSection"]] = relationship(back_populates="course")
    lab_sections: Mapped[List["LabSection"]] = relationship(back_populates="course")
    department_id : Mapped[int] = mapped_column("department_id", ForeignKey('department.id'))
    _department : Mapped[Department] = relationship(lazy="subquery")
    __instructor_id : Mapped[int] = mapped_column("instructor_id", ForeignKey('instructor.id'))
    _instructor : Mapped[Instructor] = relationship(lazy="subquery")


    def __init__(self, id : int, name: str, description: str, department_id : int, instructor_id : int, lab_required : bool = False, consent_required : bool = False) -> None:
        super().__init__()
        self.__id : int = id
        self.__name : str = name
        self.__description : str = description
        self.department_id : int = department_id
        self.__instructor_id : int = instructor_id
        self.__lab_required : int = lab_required
        self.__consent_required : str = consent_required
        self.__pre_reqs : List['Course'] = []

    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def description(self) -> str:
        return self.__description

    @property
    def consent_required(self) -> bool:
        return self.__consent_required

    @property
    def pre_reqs(self) -> List['Course']:
        return self.__pre_reqs

    @property
    def instructor_id(self) -> bool:
        return self.__instructor_id

    @property
    def lab_required(self) -> bool:
        return self.__lab_required

    def view(self) -> Dict[str, object]:
        return {"id": self.id, "name": self.name, "description": self.description}

    def add_pre_req(self, course : "Course") -> None:
        self.__pre_reqs.append(course)

class TimeSlot(ManagedEntity):
    __id : Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)
    __day : Mapped[str] = mapped_column("day", String(20))
    __start_time : Mapped[time] = mapped_column("start_time")
    __end_time : Mapped[time] = mapped_column("end_time")
    __course_section_id : Mapped[int] = mapped_column("course_section_id", ForeignKey('course_section.id'), nullable=True)
    __lab_section_id : Mapped[int] = mapped_column("lab_section_id", ForeignKey('lab_section.id'), nullable=True)


    def __init__(self, day : str, start_time : time, end_time : time):
        super().__init__()
        self.__day : str = day
        self.__start_time : time = start_time
        self.__end_time : time = end_time

    @property
    def id(self) -> int:
        return self.__id

    @property
    def day(self) -> str:
        return self.__day

    @property
    def start_time(self) -> str:
        return self.__start_time.strftime('%-I:%M%p')

    @property
    def end_time(self) -> str:
        return self.__end_time.strftime('%-I:%M%p')

    def view(self) -> Dict[str, object]:
        return {"day": self.day, "start_time": self.start_time,\
            "end_time": self.end_time}

    def __repr__(self) -> str:
        return self.day + " " + self.start_time + "-" + self.end_time


class Section:
    id : Mapped[int] = mapped_column("id", primary_key=True)
    _capacity : Mapped[int] = mapped_column("capacity")

    def __init__(self, id: int, capacity : int, course : Course, times : List[TimeSlot]) -> None:
        super().__init__()
        self.id : int = id
        self._capacity : int = capacity
        self._times : List[TimeSlot] = times
        self.course : Course = course
        self._registrations : List[Registration] = []

    @property
    def times(self) -> List[TimeSlot]:
        return self._times

    def at_capacity(self) -> bool:
        return len(self._registrations) >= self._capacity

    def add_registration(self, r : Registration) -> None:
        self._registrations.append(r)

    def view(self) -> Dict[str, object]:
        return {'id': self.id, "course": self.course.view(), "times": [t.view() for t in self.times]}

class LabSection(Section, ManagedEntity):
    course_id : Mapped[int] = mapped_column("course_id", ForeignKey("course.id"))
    course : Mapped["Course"] = relationship(lazy="subquery")
    _times : Mapped[List["TimeSlot"]] = relationship(lazy="subquery")
    _registrations : Mapped[List["Registration"]] = relationship(lazy="subquery")

    def __init__(self, section_id: int, capacity : int, course : Course, times : List[TimeSlot]) -> None:
        id : int = course.id * 100 + section_id
        super().__init__(id, capacity, course, times)

class CourseSection(Section, ManagedEntity):
    course_id : Mapped[int] = mapped_column("course_id", ForeignKey("course.id"))
    course : Mapped["Course"] = relationship(lazy="subquery")
    _times : Mapped[List["TimeSlot"]] = relationship(lazy="subquery")
    _registrations : Mapped[List["Registration"]] = relationship(lazy="subquery")

    def __init__(self, section_id: int, capacity : int, course : Course, times : List[TimeSlot]) -> None:
        id : int = course.id * 10 + section_id
        super().__init__(id, capacity, course, times)

    @property
    def consent_required(self) -> bool:
        return self.course.consent_required
