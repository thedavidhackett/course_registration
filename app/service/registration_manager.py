# from typing import Tuple
# from .registration_service import RegistrationService
# from .requirement_checker import RequirementChecker
# from model.course import CourseSection
# from model.registration import Registration
# from model.user import Student

# class RegistrationManager:
#     def __init__(self, rs : RegistrationService, req_checker : RequirementChecker) -> None:
#         self.__rs = rs
#         self.__req_checker = req_checker

#     def register(self, student_id : int, course_id : int) -> Tuple[bool, str]:
#         student : Student = self.__em.get_by_id(Student, student_id)
#         course : CourseSection = self.__em.get_by_id(CourseSection, course_id)

#         create_registration : bool
#         status : str

#         create_registration, status = first_checker.check_requirements(student, course)

#         if create_registration:
#             registration : Registration = Registration(student_id=student_id, course_section_id=course_id, status=status)
#             self.__em.add(registration)

#         return status
