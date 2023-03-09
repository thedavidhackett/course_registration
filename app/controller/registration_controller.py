from abc import ABC, abstractmethod
from typing import Any, Dict

from flask import g, request
from flask_restful import Api, Resource

from model.notification import Notification
from service.registration_service import RegistrationServiceInterface
from service.requirement_checker import RequirementChecker

class RegisterCourseHandler(ABC):
    def __init__(self, rs : RegistrationServiceInterface, checker : RequirementChecker) -> None:
        super().__init__()
        self._rs : RegistrationServiceInterface = rs
        self._checker : RequirementChecker = checker

    @abstractmethod
    def post(self):
        data : Dict[str, Any] = request.get_json()
        notification : Notification = self._rs.register(self._checker, g.user.id, data.get("course_section_id"), data.get("lab_id"))

        return notification.view()


class BaseRegisterCourseHandler(RegisterCourseHandler, Resource):
    def __init__(self, rs: RegistrationServiceInterface, checker: RequirementChecker) -> None:
        super().__init__(rs, checker)

    def post(self):
        data : Dict[str, Any] = request.get_json()
        notification : Notification = self._rs.register(self._checker, g.user.id, data.get("course_section_id"), data.get("lab_id"))

        return notification.view()

class PendingRegisterCourseHandler(RegisterCourseHandler, Resource):
    def __init__(self, rs: RegistrationServiceInterface, checker: RequirementChecker) -> None:
        super().__init__(rs, checker)

    def post(self):
        data : Dict[str, Any] = request.get_json()
        notification : Notification = self._rs.register(self._checker, g.user.id, data.get("course_section_id"), data.get("lab_id"))

        return notification.view()

class TentativeRegisterCourseHandler(RegisterCourseHandler, Resource):
    def __init__(self, rs: RegistrationServiceInterface, checker: RequirementChecker) -> None:
        super().__init__(rs, checker)

    def post(self):
        data : Dict[str, Any] = request.get_json()
        notification : Notification = self._rs.register(self._checker, g.user.id, data.get("course_section_id"), data.get("lab_id"))

        return notification.view()

class DropCourseHandler(Resource):
    def __init__(self, rs : RegistrationServiceInterface) -> None:
        super().__init__()
        self.__rs : RegistrationServiceInterface = rs

    def post(self, id : int):
        notification : Notification = self.__rs.drop_class(g.user.id, id)

        return notification.view()


def register(api : Api, rs : RegistrationServiceInterface, checker : RequirementChecker, pending_checker : RequirementChecker, tentative_checker : RequirementChecker) -> None:
    api.add_resource(BaseRegisterCourseHandler, "/api/register", resource_class_kwargs={'rs': rs, 'checker': checker})
    api.add_resource(PendingRegisterCourseHandler, "/api/register/pending", resource_class_kwargs={'rs': rs, 'checker': pending_checker})
    api.add_resource(TentativeRegisterCourseHandler, "/api/register/tentative", resource_class_kwargs={'rs': rs, 'checker': tentative_checker})
    api.add_resource(DropCourseHandler, "/api/drop-course/<int:id>", resource_class_kwargs={'rs': rs})
