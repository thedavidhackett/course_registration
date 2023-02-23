from typing import Dict, List
from datetime import time
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import column_property


from .base import ManagedEntity
from .registration import Registration


class Course(ManagedEntity):
    __id : Mapped[int] = mapped_column("id", primary_key=True)
    __name : Mapped[str] = mapped_column("name", String(100))
    __description : Mapped[str] = mapped_column("description", String(255))

    def __init__(self, id : int, name: str, description: str) -> None:
        super().__init__()
        self.__id : int = id
        self.__name : str = name
        self.__description : str = description

    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def description(self) -> str:
        return self.__description

    def view(self) -> Dict[str, object]:
        return {"id": self.id, "name": self.name, "description": self.description}

class TimeSlot(ManagedEntity):
    __id : Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)
    __day : Mapped[str] = mapped_column("day", String(20))
    __start_time : Mapped[time] = mapped_column("start_time")
    __end_time : Mapped[time] = mapped_column("end_time")
    __course_section_id : Mapped[int] = mapped_column("course_section_id", ForeignKey('course_section.id'))

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

class CourseSection(ManagedEntity):
    __id : Mapped[int] = mapped_column("id", primary_key=True)
    __capacity : Mapped[int] = mapped_column("capacity")
    __course_id : Mapped[int] = mapped_column("course_id", ForeignKey("course.id"))
    _course: Mapped["Course"] = relationship(lazy="subquery")
    __times : Mapped[List["TimeSlot"]] = relationship(lazy="subquery")
    __registrations : Mapped[List["Registration"]] = relationship(lazy="subquery")

    def __init__(self, id: int, capacity : int, course : Course, times : List[TimeSlot]) -> None:
        super().__init__()
        self.__id : int = id
        self.__capacity : int = capacity
        self.__times : List[TimeSlot] = times
        self._course : Course = course
        self.__registrations : List[Registration] = []


    @property
    def id(self) -> int:
        return self.__id

    @property
    def course(self) -> Dict[str, object]:
        return self._course.view()

    @property
    def times(self) -> List[Dict[str, object]]:
        details : List[Dict[str, object]] = []
        time : TimeSlot
        for time in self.__times:
            details.append(time.view())

        return details

    def view(self) -> Dict[str, object]:
        return {'id': self.id, "course": self.course, "times": self.times}

    def add_registration(self, r : Registration) -> None:
        self.__registrations.append(r)
