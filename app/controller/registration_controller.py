from abc import ABC, abstractmethod
from typing import Any, Dict

from flask import g, request
from flask_restful import Api, Resource

from model.notification import Notification
from service.registration_service import RegistrationServiceInterface
from service.notification_service import NotificationServiceInterface
from service.permission_service import PermissionServiceInterface
from service.requirement_checker import RequirementChecker

class RegisterCourseHandler(ABC):
    def __init__(self, rs : RegistrationServiceInterface, checker : RequirementChecker) -> None:
        super().__init__()
        self._rs : RegistrationServiceInterface = rs
        self._checker : RequirementChecker = checker

    @abstractmethod
    def on_success(self, student_id : int, course_id : int) -> None:
        pass

    def post(self):
        data : Dict[str, Any] = request.get_json()
        course_id = data["course_section_id"]

        notification : Notification
        success : bool
        notification, success = self._rs.register(self._checker, g.user.id, course_id, data.get("lab_id"))

        if success:
            self.on_success(g.user.id, course_id)

        return notification.view()



class BaseRegisterCourseHandler(RegisterCourseHandler, Resource):
    def __init__(self, rs: RegistrationServiceInterface, checker: RequirementChecker) -> None:
        super().__init__(rs, checker)

    def on_success(self, student_id : int, course_id : int) -> None:
        return

    def post(self):
        data : Dict[str, Any] = request.get_json()
        notification : Notification
        success : bool
        notification, success = self._rs.register(self._checker, g.user.id, data.get("course_section_id"), data.get("lab_id"))

        return notification.view()

class PendingRegisterCourseHandler(RegisterCourseHandler, Resource):
    def __init__(self, rs: RegistrationServiceInterface, ps : PermissionServiceInterface, checker: RequirementChecker) -> None:
        super().__init__(rs, checker)
        self.__ps : PermissionServiceInterface = ps

    def on_success(self, student_id: int, course_id: int) -> None:
        self.__ps.create_overload_permission(student_id, course_id)

class TentativeRegisterCourseHandler(RegisterCourseHandler, Resource):
    def __init__(self, rs: RegistrationServiceInterface, ps : PermissionServiceInterface, checker: RequirementChecker) -> None:
        super().__init__(rs, checker)
        self.__ps : PermissionServiceInterface = ps

    def on_success(self, student_id: int, course_id: int) -> None:
        self.__ps.create_instructor_permission(student_id, course_id)

class DropCourseHandler(Resource):
    def __init__(self, rs : RegistrationServiceInterface) -> None:
        super().__init__()
        self.__rs : RegistrationServiceInterface = rs

    def post(self, id : int):
        notification : Notification = self.__rs.drop_class(g.user.id, id)

        return notification.view()


def register(api : Api, rs : RegistrationServiceInterface, ps : PermissionServiceInterface, checker : RequirementChecker, pending_checker : RequirementChecker, tentative_checker : RequirementChecker) -> None:
    api.add_resource(BaseRegisterCourseHandler, "/api/register", resource_class_kwargs={'rs': rs, 'checker': checker})
    api.add_resource(PendingRegisterCourseHandler, "/api/register/pending", resource_class_kwargs={'rs': rs, 'ps': ps, 'checker': pending_checker})
    api.add_resource(TentativeRegisterCourseHandler, "/api/register/tentative", resource_class_kwargs={'rs': rs, 'ps': ps, 'checker': tentative_checker})
    api.add_resource(DropCourseHandler, "/api/drop-course/<int:id>", resource_class_kwargs={'rs': rs})
