from abc import ABC, abstractmethod
from typing import List

from sqlalchemy import select
from sqlalchemy.sql.expression import Select

from .entity_manager import EntityManagerInterface
from model.course import CourseSection


class CourseServiceInterface(ABC):
    @abstractmethod
    def search(self, course_id : int) -> List[CourseSection]:
        pass

class CourseService(CourseServiceInterface):
    def __init__(self, em : EntityManagerInterface) -> None:
        self.__em : EntityManagerInterface = em

    def search(self, course_id : int) -> List[CourseSection]:
        stmt : Select = select(CourseSection).where(CourseSection.course_id == course_id)
        return self.__em.get_by_criteria(stmt)
