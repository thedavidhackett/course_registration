from abc import ABC, abstractmethod
from typing import Optional, Tuple

from sqlalchemy import select
from sqlalchemy.sql.expression import Select

from .entity_manager import EntityManagerInterface
from .notification_factory import NotificationCreator
from .permission_service import PermissionServiceInterface
from .requirement_checker import RequirementChecker
from .course_service import CourseServiceInterface
from .notification_service import NotificationServiceInterface
from model.course import CourseSection, Department, LabSection
from model.notification import Notification
from model.permission import Permission, InstructorPermission, OverloadPermission
from model.registration import Registration
from model.user import Student


class RegistrationServiceInterface(ABC):
    @abstractmethod
    def register(self, checker_chain : RequirementChecker, student_id : int, course_id : int, lab_id = None) -> Tuple[Notification, bool]:
        pass

    @abstractmethod
    def get_registration_by_student_id_and_course_id(self, student_id : int, course_id : int) -> Optional[Registration]:
        pass

    @abstractmethod
    def drop_class(self, student_id : int, course_id : int) -> Notification:
        pass


class RegistrationService(RegistrationServiceInterface, PermissionServiceInterface):
    def __init__(self, em : EntityManagerInterface, cs : CourseServiceInterface, ns : NotificationServiceInterface, notification_factory : NotificationCreator) -> None:
        self.__em : EntityManagerInterface = em
        self.__cs : CourseServiceInterface = cs
        self.__ns : NotificationServiceInterface = ns
        self.__notification_factory = notification_factory

    def register(self, checker_chain : RequirementChecker, student_id : int, cs_id : int, lab_id : Optional[int] = None) -> Tuple[Notification, bool]:

        if (self.get_registration_by_student_id_and_course_id(student_id, cs_id)):
            return self.__notification_factory.factory_method({"msg": "You are already registered for this class", "type": "warning"}), False

        student : Optional[Student] = self.__em.get_by_id(Student, student_id)
        course : Optional[CourseSection] = self.__cs.get_course_section_by_id(cs_id)
        lab : Optional[LabSection] = None

        if lab_id:
            lab = self.__em.get_by_id(LabSection, lab_id)

        if not student or not course:
            return self._error(), False

        create_registration : bool
        notification : Notification
        status : str

        create_registration, notification, status = checker_chain.check_requirements(student, course, lab)

        if create_registration:
            registration : Registration = Registration(student_id=student_id, course_section_id=cs_id, lab_id = lab_id, status=status)
            self.__em.add(registration)

        return notification, create_registration

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

    def get_permission_by_instructor_and_student_id(self, instructor_id: int, student_id : int) -> Optional[Permission]:
        stmt : Select = select(Permission).where(Permission.approver_id == instructor_id).where(Permission.student_id == student_id)
        return self.__em.get_one_by_criteria(stmt)

    def create_overload_permission(self, student_id: int, course_section_id: int) -> None:
        course_section : Optional[CourseSection] = self.__cs.get_course_section_by_id(course_section_id)
        department : Optional[Department] = self.__cs.get_department_by_id(course_section.course.department_id)

        permission : OverloadPermission = OverloadPermission(student_id, course_section.course_id, department.chair_id)
        self.__em.add(permission)

        self.__ns.create_notification({"msg": f"A student is requesting overload for {course_section.course.name} - {course_section.course_id}", "type" : "info", "instructor_id": department.chair_id})


    def create_instructor_permission(self, student_id: int, course_section_id: int) -> None:
        course_section : Optional[CourseSection] = self.__cs.get_course_section_by_id(course_section_id)

        permission : InstructorPermission = InstructorPermission(student_id, course_section.course_id, course_section.course.instructor_id)
        self.__em.add(permission)

        self.__ns.create_notification({"msg": f"A student is requesting consent for {course_section.course.name} - {course_section.course_id}", "type" : "info", "instructor_id": course_section.course.instructor_id})


    def _error(self) -> Notification:
        return self.__notification_factory.factory_method({"msg": "Something went wrong", "type": "Warning"})
