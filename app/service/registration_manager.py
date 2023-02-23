from typing import Tuple
from model.course import CourseSection
from model.registration import Registration
from model.user import Student
from .entity_manager import EntityManager

class RegistrationManager:
    def __init__(self, em : EntityManager) -> None:
        self.__em : EntityManager = em

    def register(self, student_id : int, course_id : int) -> Tuple[bool, str]:
        student : Student = self.__em.get_by_id(Student, student_id)
        course : CourseSection = self.__em.get_by_id(CourseSection, course_id)

        status = "registered"
        registration : Registration = Registration(student_id=student_id, course_section_id=course_id, status=status)

        self.__em.add(registration)

        return True, "Registration Successful"
