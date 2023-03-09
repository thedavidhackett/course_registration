from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy import select
from sqlalchemy.sql.expression import Select

from .entity_manager import EntityManagerInterface
from .notification_factory import NotificationCreator
from .requirement_checker import RequirementChecker
from .course_service import CourseServiceInterface
from .student_service import StudentService
from model.course import CourseSection, LabSection
from model.notification import Notification
from model.registration import Registration
from model.user import Student


class RegistrationServiceInterface(ABC):
    @abstractmethod
    def register(self, checker_chain : RequirementChecker, student_id : int, course_id : int, lab_id = None) -> Notification:
        pass

    @abstractmethod
    def get_registration_by_student_id_and_course_id(self, student_id : int, course_id : int) -> Optional[Registration]:
        pass

    @abstractmethod
    def drop_class(self, student_id : int, course_id : int) -> Notification:
        pass


class RegistrationService:
    def __init__(self, em : EntityManagerInterface, cs : CourseServiceInterface, ss : StudentService, notification_factory : NotificationCreator) -> None:
        self.__em : EntityManagerInterface = em
        self.__cs : CourseServiceInterface = cs
        self.__notification_factory = notification_factory

    def register(self, checker_chain : RequirementChecker, student_id : int, cs_id : int, lab_id : Optional[int] = None) -> Notification:

        if (self.get_registration_by_student_id_and_course_id(student_id, cs_id)):
            return self.__notification_factory.factory_method({"msg": "You are already registered for this class", "type": "warning"})

        student : Student = self.__em.get_by_id(Student, student_id)
        course : CourseSection = self.__cs.get_course_section_by_id(cs_id)
        lab : Optional[LabSection] = None

        if lab_id:
            lab = self.__em.get_by_id(LabSection, lab_id)

        create_registration : bool
        notification : Notification
        status : str

        create_registration, notification, status = checker_chain.check_requirements(student, course, lab)

        if create_registration:
            registration : Registration = Registration(student_id=student_id, course_section_id=cs_id, lab_id = lab_id, status=status)
            self.__em.add(registration)

        return notification

    def drop_class(self, student_id : int, course_id : int) -> Notification:
        registration : Optional[Registration] = self.get_registration_by_student_id_and_course_id(student_id, course_id)

        if registration:
            self.__em.delete(registration)
            return self.__notification_factory.factory_method({"msg": f"Course {course_id} was successfully dropped", "type": "success"})

        return self.__notification_factory.factory_method({"msg": "You are not enrolled in this course", "type": "warning"})

    def get_registration_by_student_id_and_course_id(self, student_id : int, course_id : int) -> Optional[Registration]:
        stmt : Select = select(Registration).where(Registration.course_section_id == course_id).where(Registration.student_id == student_id)
        registration : Optional[Registration] = self.__em.get_one_by_criteria(stmt)

        return registration
