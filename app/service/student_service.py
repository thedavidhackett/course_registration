from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.expression import Select

from .entity_manager import EntityManagerInterface
from .notification_service import NotificationServiceInterface
from model.course import CourseSection
from model.registration import Registration
from model.user import Student
from model.notification import Notification

class StudentServiceInterface(ABC):
    @abstractmethod
    def get_student_by_id(self, id : int) -> Optional[Student]:
        pass

    @abstractmethod
    def get_student_courses(self, id : int) -> Dict[str, List[CourseSection]]:
        pass

    @abstractmethod
    def get_student_notifications(self, student_id : int) -> List[Notification]:
        pass

class StudentService:
    def __init__(self, em : EntityManagerInterface, ns : NotificationServiceInterface) -> None:
        self.__em : EntityManagerInterface = em
        self.__ns : NotificationServiceInterface = ns

    def get_student_by_id(self, id : int) -> Student:
        return self.__em.get_by_id(Student, id)

    def get_student_courses(self, student : Student) -> Dict[str, List[CourseSection]]:
        registered_ids : List[int] = []
        tentative_ids : List[int] = []
        pending_ids : List[int] = []
        reg : Registration
        for reg in student.registrations:
            if reg.status == "registered":
                registered_ids.append(reg.course_section_id)
            elif reg.status == "tentative":
                tentative_ids.append(reg.course_section_id)
            elif reg.status == "pending":
                pending_ids.append(reg.course_section_id)

        result : Dict[str, List[CourseSection]] = {
            "registered": [],
            "tentative": [],
            "pending": []
        }
        key : str
        ids : List[int]
        for key, ids in zip(result.keys(), [registered_ids, tentative_ids, pending_ids]):
            stmt : Select = Select(CourseSection).options(joinedload(CourseSection.course)).where(CourseSection.id.in_(ids))
            result[key] = self.__em.get_by_criteria(stmt)

        return result


    def get_student_notifications(self, student_id : int) -> List[Notification]:
        return self.__ns.get_student_notifications(student_id)
