from abc import abstractmethod
from typing import Optional, Protocol, Tuple

from model.course import CourseSection
from model.restriction import Restriction
from model.user import Student

class RequirementChecker(Protocol):

    __next : Optional["RequirementChecker"]

    @abstractmethod
    def check_requirements(self, student : Student, course : CourseSection,) -> Tuple[bool, str]:
        pass

class BaseChecker:
    def __init__(self, next : RequirementChecker = None) -> None:
        self.__next : Optional[RequirementChecker] = next

    def check_requirements(self, student : Student, course : CourseSection) -> Tuple[bool, str]:
        return True, "registered"

class RestrictionChecker:
    def __init__(self, next : RequirementChecker) -> None:
        self.__next : Optional[RequirementChecker] = next

    def check_requirements(self, student : Student, course : CourseSection) -> Tuple[bool, str]:
        r : Restriction
        for r in student.restrictions:
            if not r.can_register():
                return False, r.message

        return self.__next.check_requirements(student, course)

class StudentCapacityChecker:
    def __init__(self, next : RequirementChecker) -> None:
        self.__next : Optional[RequirementChecker] = next

    def check_requirements(self, student : Student, course : CourseSection) -> Tuple[bool, str]:
        if student.at_capacity():
            return True, "pending"

        return self.__next.check_requirements(student, course)

class CourseConsentChecker:
    def __init__(self, next : RequirementChecker) -> None:
        self.__next : Optional[RequirementChecker] = next

    def check_requirements(self, student : Student, course : CourseSection) -> Tuple[bool, str]:
        if course.consent_required:
            return True, "tentative"

        return self.__next.check_requirements(student, course)


def create_registration_requirements_chain() -> RequirementChecker:
    base_checker : BaseChecker = BaseChecker()
    course_consent_checker : CourseConsentChecker = CourseConsentChecker(base_checker)
    student_capacity_checker : StudentCapacityChecker = StudentCapacityChecker(course_consent_checker)
    restriction_checker : RestrictionChecker = RestrictionChecker(student_capacity_checker)

    return restriction_checker
