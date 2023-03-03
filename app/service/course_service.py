from typing import Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.sql.expression import Select

from .entity_manager import EntityManager
from model.course import CourseSection

class CourseService:
    def __init__(self, em : EntityManager) -> None:
        self.__em = em

    def search(self, course_id : int) -> List[CourseSection]:
        stmt : Select = select(CourseSection).where(CourseSection.course_id == course_id)
        return self.__em.get_by_criteria(stmt)
