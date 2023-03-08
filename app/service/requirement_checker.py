from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple

from model.course import Course, CourseSection, LabSection, TimeSlot
from model.notification import Notification
from model.restriction import Restriction
from model.user import Student
from service.notification_factory import (BasicNotificationCreator,
                                          DialogFormNotificationCreator,
                                          DialogNotificationCreator,
                                          NotificationCreator)

class RequirementChecker(ABC):
    __notification_factory : NotificationCreator

    @abstractmethod
    def check_requirements(self, student : Student, course : CourseSection,) -> Tuple[bool, Notification, str]:
        pass

class BaseChecker(RequirementChecker):
    def __init__(self, notification_factory : NotificationCreator) -> None:
        self.__notification_factory : NotificationCreator = notification_factory

    def check_requirements(self, student : Student, course : CourseSection, lab : LabSection = None) -> Tuple[bool, Notification, str]:
        return True, self.__notification_factory.factory_method(\
            {"msg": f"You successfully registered for {course.id} - {course.course.name}", "type": "success"}),\
            "registered"

class PendingBaseChecker(RequirementChecker):
    def __init__(self, notification_factory : NotificationCreator) -> None:
        self.__notification_factory : NotificationCreator = notification_factory

    def check_requirements(self, student : Student, course : CourseSection, lab : LabSection = None) -> Tuple[bool, Notification, str]:
        return True, self.__notification_factory.factory_method(\
            {"msg": f"Your registration for {course.id} - {course.course.name} is pending", "type": "success"}),\
            "pending"

class TentativeBaseChecker(RequirementChecker):
    def __init__(self, notification_factory : NotificationCreator) -> None:
        self.__notification_factory : NotificationCreator = notification_factory

    def check_requirements(self, student : Student, course : CourseSection, lab : LabSection = None) -> Tuple[bool, Notification, str]:
        return True, self.__notification_factory.factory_method(\
            {"msg": f"Your registration for {course.id} - {course.course.name} is tentative", "type": "success"}),\
            "tentative"

class RestrictionChecker(RequirementChecker):
    def __init__(self, notification_factory : NotificationCreator, next : RequirementChecker, lab : LabSection = None) -> None:
        self.__notification_factory : NotificationCreator = notification_factory
        self.__next : RequirementChecker = next

    def check_requirements(self, student : Student, course : CourseSection, lab : LabSection = None) -> Tuple[bool, Notification, str]:
        r : Restriction
        for r in student.restrictions:
            print(r.message)
            if not r.can_register():
                return False, self.__notification_factory.factory_method({"msg": r.message, "type": "warning"}), ""

        return self.__next.check_requirements(student, course, lab)

class StudentCapacityChecker(RequirementChecker):
    def __init__(self, notification_factory : NotificationCreator, next : RequirementChecker) -> None:
        self.__notification_factory : NotificationCreator = notification_factory
        self.__next : RequirementChecker = next

    def check_requirements(self, student : Student, course : CourseSection, lab : LabSection = None) -> Tuple[bool, Notification, str]:
        lab_id = lab.id if lab else None
        if student.at_capacity():
            notification : Notification = self.__notification_factory.factory_method(\
                {"msg": "Adding this course would overload your schedule. Would you like to request permission?", \
                 "type": "warning", "data": {"course_section_id": course.id}, "action": "/register/pending", "submit_text": "Request Permission"})

            return False, notification, ""

        return self.__next.check_requirements(student, course, lab)

class CourseConsentChecker(RequirementChecker):
    def __init__(self, notification_factory : NotificationCreator, next : RequirementChecker) -> None:
        self.__notification_factory : NotificationCreator = notification_factory
        self.__next : RequirementChecker = next

    def check_requirements(self, student : Student, course : CourseSection, lab : LabSection = None) -> Tuple[bool, Notification, str]:
        lab_id = lab.id if lab else None
        if course.consent_required:
            notification : Notification = self.__notification_factory.factory_method(\
                {"msg": "This course requires instructor approval? Would you like to request it",\
                  "type": "warning", "data": {"course_section_id": course.id}, "action": "/register/tentative", "submit_text": "Request Approval"})

            return False, notification, ""

        return self.__next.check_requirements(student, course, lab)

class PreReqChecker(RequirementChecker):
    def __init__(self, notification_factory : NotificationCreator, next : RequirementChecker) -> None:
        self.__notification_factory : NotificationCreator = notification_factory
        self.__next : RequirementChecker = next

    def check_requirements(self, student : Student, course : CourseSection, lab : LabSection = None) -> Tuple[bool, Notification, str]:
        c : Course
        courses_taken : List[int] = [reg.course_section_id // 10 for reg in student.registrations if reg.status == "completed"]
        for c in course.get_pre_reqs():
            if c.id not in courses_taken:
                return False, self.__notification_factory.factory_method(\
                    {"msg": "You have not met the prereqs for this course", "type": "warning"}), ""

        return self.__next.check_requirements(student, course, lab)


class CourseCapacityChecker(RequirementChecker):
    def __init__(self, notification_factory : NotificationCreator, next : RequirementChecker) -> None:
        self.__notification_factory : NotificationCreator = notification_factory
        self.__next : RequirementChecker = next

    def check_requirements(self, student : Student, course : CourseSection, lab : LabSection = None) -> Tuple[bool, Notification, str]:
        if course.at_capacity():
            options : List[Dict[str, int]] = [{"label" : str(c.id) + " " + " and ".join([str(t) for t in c.times]), "value": c.id}\
                                               for c in course.course.course_sections if c.id != course.id]

            msg : str = "This course is full"
            if len(options) > 0:
                msg += ", here are other sections"

            return False, self.__notification_factory.factory_method(\
                    {"msg": msg, "type": "warning", "data": {}, "action": "/register", "options": options, "value_name": "course_section_id", "submit_text": "Select Section"}), ""

        if lab and lab.at_capacity():
            options : List[Dict[str, int]] = [{"label" : str(l.id) + " " + " and ".join([str(t) for t in l.times]), "value": l.id}\
                                               for l in course.course.lab_sections if l.id != lab.id]

            msg : str = "This lab is full"
            if len(options) > 0:
                msg += ", here are other sections"

            return False, self.__notification_factory.factory_method(\
                    {"msg": msg, "type": "warning", "data": {"course_section_id": course.id}, options : options, "action": "/register", "value_name": "lab_id", "submit_text": "Select Lab"}), ""

        return self.__next.check_requirements(student, course, lab)

class LabRequirementChecker(RequirementChecker):
    def __init__(self, notification_factory : NotificationCreator, next : RequirementChecker) -> None:
        self.__notification_factory : NotificationCreator = notification_factory
        self.__next : RequirementChecker = next

    def check_requirements(self, student : Student, course : CourseSection, lab : LabSection = None) -> Tuple[bool, Notification, str]:
        t : TimeSlot
        if course.course.lab_required and not lab:
            options : List[Dict[str, int]] = [{"label" : str(l.id) + " " + " and ".join([str(t) for t in l.times]), "value": l.id}\
                                        for l in course.course.lab_sections]
            notification : Notification = self.__notification_factory.factory_method(\
                    {"msg": "This course requires a lab, please select one.", "type": "info", "data": {"course_id": course.id},\
                      "action": "/register", "value_name": "lab_id", "options": options, "submit_text": "Select Lab"})

            return False, notification, ""

        return self.__next.check_requirements(student, course, lab)


def create_registration_requirements_chain() -> RequirementChecker:
    base_checker : BaseChecker = BaseChecker(BasicNotificationCreator())
    course_consent_checker : CourseConsentChecker = CourseConsentChecker(DialogNotificationCreator(), base_checker)
    student_capacity_checker : StudentCapacityChecker = StudentCapacityChecker(DialogNotificationCreator(), course_consent_checker)
    lab_requirement_checker : LabRequirementChecker = LabRequirementChecker(DialogFormNotificationCreator(), student_capacity_checker)
    course_capacity_checker : CourseCapacityChecker = CourseCapacityChecker(DialogFormNotificationCreator(), lab_requirement_checker)
    pre_req_checker : PreReqChecker = PreReqChecker(BasicNotificationCreator(),course_capacity_checker)
    restriction_checker : RestrictionChecker = RestrictionChecker(BasicNotificationCreator(), pre_req_checker)

    return restriction_checker

def create_pending_requirements_chain() -> RequirementChecker:
    base_pending_checker : PendingBaseChecker = PendingBaseChecker(BasicNotificationCreator())
    course_capacity_checker : CourseCapacityChecker = CourseCapacityChecker(DialogFormNotificationCreator(), base_pending_checker)
    pre_req_checker : PreReqChecker = PreReqChecker(BasicNotificationCreator(),course_capacity_checker)
    restriction_checker : RestrictionChecker = RestrictionChecker(BasicNotificationCreator(), pre_req_checker)

    return restriction_checker

def create_tentative_requirements_chain() -> RequirementChecker:
    base_pending_checker : TentativeBaseChecker = TentativeBaseChecker(BasicNotificationCreator())
    course_capacity_checker : CourseCapacityChecker = CourseCapacityChecker(DialogFormNotificationCreator(), base_pending_checker)
    pre_req_checker : PreReqChecker = PreReqChecker(BasicNotificationCreator(),course_capacity_checker)
    restriction_checker : RestrictionChecker = RestrictionChecker(BasicNotificationCreator(), pre_req_checker)

    return restriction_checker
