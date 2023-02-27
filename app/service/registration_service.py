from typing import Optional, Tuple

from sqlalchemy import select
from sqlalchemy.sql.expression import Select

from .entity_manager import EntityManager
from .requirement_checker import RequirementChecker
from model.course import CourseSection
from model.registration import Registration
from model.user import Student

class RegistrationService:
    def __init__(self, em : EntityManager) -> None:
        self.__em : EntityManager = em

    def register(self, student_id : int, course_id : int, first_checker : RequirementChecker) -> Tuple[bool, str]:
        student : Student = self.__em.get_by_id(Student, student_id)
        course : CourseSection = self.__em.get_by_id(CourseSection, course_id)

        create_registration : bool
        status : str

        create_registration, status = first_checker.check_requirements(student, course)

        if create_registration:
            registration : Registration = Registration(student_id=student_id, course_section_id=course_id, status=status)
            self.__em.add(registration)

        return status

    def get_registration_by_student_id_and_course_id(self, student_id : int, course_id : int) -> Optional[Registration]:
        stmt : Select = select(Registration).where((Registration.student_id == student_id) & (Registration.course_section_id == course_id))
        registration : Registration = self.__em.get_one_by_criteria(stmt)

        return registration
