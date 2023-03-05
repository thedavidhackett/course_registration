from abc import ABC, abstractmethod
from typing import  List, Optional, Tuple

from model.course import Course, CourseSection
from model.notification import Notification
from model.restriction import Restriction
from model.user import Student
from service.notification_factory import BasicNotificationCreator, CoursePendingNotificationCreator, CourseTentativeNotificationCreator, NotificationCreator

class RequirementChecker(ABC):
    __notification_factory : NotificationCreator

    @abstractmethod
    def check_requirements(self, student : Student, course : CourseSection,) -> Tuple[bool, Notification]:
        pass

class BaseChecker(RequirementChecker):
    def __init__(self, notification_factory : NotificationCreator) -> None:
        self.__notification_factory : NotificationCreator = notification_factory

    def check_requirements(self, student : Student, course : CourseSection) -> Tuple[bool, Notification]:
        return True, self.__notification_factory.factory_method(\
            {"msg": f"You successfully registered for {course.id} - {course.course.name}", "type": "success"})

class RestrictionChecker(RequirementChecker):
    def __init__(self, notification_factory : NotificationCreator, next : RequirementChecker) -> None:
        self.__notification_factory : NotificationCreator = notification_factory
        self.__next : RequirementChecker = next

    def check_requirements(self, student : Student, course : CourseSection) -> Tuple[bool, Notification]:
        r : Restriction
        for r in student.restrictions:
            if not r.can_register():
                return False, self.__notification_factory.factory_method({"msg": r.message, "type": "warning"})

        return self.__next.check_requirements(student, course)

class StudentCapacityChecker(RequirementChecker):
    def __init__(self, notification_factory : NotificationCreator, next : RequirementChecker) -> None:
        self.__notification_factory : NotificationCreator = notification_factory
        self.__next : RequirementChecker = next

    def check_requirements(self, student : Student, course : CourseSection) -> Tuple[bool, Notification]:
        if student.at_capacity():
            return False, self.__notification_factory.factory_method(\
                {"msg": "Adding this course would overload your schedule. Would you like to request permission?", \
                 "type": "course_pending", "course_id": course.id})

        return self.__next.check_requirements(student, course)

class CourseConsentChecker(RequirementChecker):
    def __init__(self, notification_factory : NotificationCreator, next : RequirementChecker) -> None:
        self.__notification_factory : NotificationCreator = notification_factory
        self.__next : RequirementChecker = next

    def check_requirements(self, student : Student, course : CourseSection) -> Tuple[bool, Notification]:
        if course.consent_required:
            return False, self.__notification_factory.factory_method(\
                {"msg": "This course requires instructor approval? Would you like to request it",\
                  "type": "course_tentative", "course_id": course.id})

        return self.__next.check_requirements(student, course)

class PreReqChecker(RequirementChecker):
    def __init__(self, notification_factory : NotificationCreator, next : RequirementChecker) -> None:
        self.__notification_factory : NotificationCreator = notification_factory
        self.__next : RequirementChecker = next

    def check_requirements(self, student : Student, course : CourseSection) -> Tuple[bool, Notification]:
        c : Course
        courses_taken : List[int] = [reg.course_section_id // 10 for reg in student.registrations if reg.status == "completed"]
        for c in course.get_pre_reqs():
            if c.id not in courses_taken:
                return False, self.__notification_factory.factory_method(\
                    {"msg": "You have not met the prereqs for this course", "type": "warning"})

        return self.__next.check_requirements(student, course)


class CourseCapacityChecker(RequirementChecker):
    def __init__(self, notification_factory : NotificationCreator, next : RequirementChecker) -> None:
        self.__notification_factory : NotificationCreator = notification_factory
        self.__next : RequirementChecker = next

    def check_requirements(self, student : Student, course : CourseSection) -> Tuple[bool, Notification]:
        if course.at_capacity():
            return False, self.__notification_factory.factory_method(\
                    {"msg": "This course is full", "type": "warning"})

        return self.__next.check_requirements(student, course)


def create_registration_requirements_chain() -> RequirementChecker:
    base_checker : BaseChecker = BaseChecker(BasicNotificationCreator())
    course_consent_checker : CourseConsentChecker = CourseConsentChecker(CourseTentativeNotificationCreator(), base_checker)
    student_capacity_checker : StudentCapacityChecker = StudentCapacityChecker(CoursePendingNotificationCreator(), course_consent_checker)
    course_capacity_checker : CourseCapacityChecker = CourseCapacityChecker(BasicNotificationCreator(), student_capacity_checker)
    pre_req_checker : PreReqChecker = PreReqChecker(BasicNotificationCreator(),course_capacity_checker)
    restriction_checker : RestrictionChecker = RestrictionChecker(BasicNotificationCreator(), pre_req_checker)

    return restriction_checker
