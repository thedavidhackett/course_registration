from abc import ABC, abstractmethod
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.expression import Select

from .entity_manager import EntityManagerInterface
from model.course import Course, CourseSection, Department, LabSection


class CourseServiceInterface(ABC):
    @abstractmethod
    def get_course_section_by_id(self, cs_id : int) -> Optional[CourseSection]:
        pass

    @abstractmethod
    def search(self, course_id : int) -> List[CourseSection]:
        pass

    @abstractmethod
    def get_course_prereqs(self, course_id : int) -> List[Course]:
        pass

    @abstractmethod
    def get_course_sections_by_course_id(self, course_id : int) -> List[CourseSection]:
        pass

    @abstractmethod
    def get_labs_by_course_id(self, course_id : int) -> List[LabSection]:
        pass

    @abstractmethod
    def get_departments(self) -> List[Department]:
        pass

class CourseService(CourseServiceInterface):
    def __init__(self, em : EntityManagerInterface) -> None:
        self.__em : EntityManagerInterface = em

    def get_course_section_by_id(self, cs_id : int) -> Optional[CourseSection]:
        stmt : Select = select(CourseSection).options(joinedload(CourseSection.course)).where(CourseSection.id == cs_id)
        return self.__em.get_by_id(CourseSection, cs_id)

    def search(self, course_id : Optional[int] = None, department_id : Optional[int] = None) -> List[CourseSection]:
        stmt : Select = select(CourseSection).join(Course)
        if course_id:
            stmt = stmt.where(CourseSection.course_id == course_id)
        if department_id:
            stmt = stmt.where(Course.department_id == department_id)
        return self.__em.get_by_criteria(stmt)

    def get_course_prereqs(self, course_id : int) -> List[Course]:
        stmt : Select = select(Course).where(Course.pre_req_for_id == course_id)
        return self.__em.get_by_criteria(stmt)

    def get_course_sections_by_course_id(self, course_id : int) -> List[CourseSection]:
        stmt : Select = select(CourseSection).where(CourseSection.course_id == course_id)
        return self.__em.get_by_criteria(stmt)

    def get_labs_by_course_id(self, course_id: int) -> List[LabSection]:
        stmt : Select = select(LabSection).where(LabSection.course_id == course_id)
        return self.__em.get_by_criteria(stmt)

    def get_departments(self) -> List[Department]:
        return self.__em.get_all(Department)
