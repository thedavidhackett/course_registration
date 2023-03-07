from typing import Dict, List
from datetime import time

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, relationship

from .base import ManagedEntity
from .registration import Registration

class Course(ManagedEntity):
    __id : Mapped[int] = mapped_column("id", primary_key=True)
    __name : Mapped[str] = mapped_column("name", String(100))
    __description : Mapped[str] = mapped_column("description", String(255))
    __consent_required : Mapped[bool] = mapped_column("consent_required")
    __pre_reqs : Mapped[List["Course"]] = relationship(lazy="subquery")
    __pre_req_for_id : Mapped[int] = mapped_column("pre_req_for_id", ForeignKey('course.id'), nullable=True)
    course_sections: Mapped[List["CourseSection"]] = relationship(back_populates="_course")
    lab_sections: Mapped[List["LabSection"]] = relationship(back_populates="_course")


    def __init__(self, id : int, name: str, description: str, consent_required : bool = False) -> None:
        super().__init__()
        self.__id : int = id
        self.__name : str = name
        self.__description : str = description
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

    def view(self) -> Dict[str, object]:
        return {"id": self.id, "name": self.name, "description": self.description, "pre_reqs" : [c.name for c in self.pre_reqs]}

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


class Section:
    id : Mapped[int] = mapped_column("id", primary_key=True)
    _capacity : Mapped[int] = mapped_column("capacity")

    def __init__(self, id: int, capacity : int, course : Course, times : List[TimeSlot]) -> None:
        super().__init__()
        self.id : int = id
        self._capacity : int = capacity
        self._times : List[TimeSlot] = times
        self._course : Course = course
        self._registrations : List[Registration] = []

    @property
    def course(self):
        return self._course

    @property
    def times(self) -> List[Dict[str, object]]:
        details : List[Dict[str, object]] = []
        time : TimeSlot
        for time in self._times:
            details.append(time.view())

        return details

    def get_pre_reqs(self) -> List[Course]:
        return self.course.pre_reqs

    def at_capacity(self) -> bool:
        return len(self._registrations) >= self._capacity

    def add_registration(self, r : Registration) -> None:
        self._registrations.append(r)

    def view(self) -> Dict[str, object]:
        return {'id': self.id, "course": self.course.view(), "times": self.times}

class LabSection(Section, ManagedEntity):
    course_id : Mapped[int] = mapped_column("course_id", ForeignKey("course.id"))
    _course : Mapped["Course"] = relationship(lazy="subquery")
    _times : Mapped[List["TimeSlot"]] = relationship(lazy="subquery")
    _registrations : Mapped[List["Registration"]] = relationship(lazy="subquery")

    def __init__(self, section_id: int, capacity : int, course : Course, times : List[TimeSlot]) -> None:
        id : int = course.id * 100 + section_id
        super().__init__(id, capacity, course, times)

class CourseSection(Section, ManagedEntity):
    course_id : Mapped[int] = mapped_column("course_id", ForeignKey("course.id"))
    _course : Mapped["Course"] = relationship(lazy="subquery")
    _times : Mapped[List["TimeSlot"]] = relationship(lazy="subquery")
    _registrations : Mapped[List["Registration"]] = relationship(lazy="subquery")

    def __init__(self, section_id: int, capacity : int, course : Course, times : List[TimeSlot]) -> None:
        id : int = course.id * 10 + section_id
        super().__init__(id, capacity, course, times)

    @property
    def consent_required(self) -> bool:
        return self._course.consent_required
