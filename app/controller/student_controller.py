from typing import Any, Dict, List

from flask import g
from flask_restful import Api, Resource

from model.course import CourseSection
from model.notification import Notification
from model.restriction import Restriction
from service.student_service import StudentServiceInterface


class StudentCoursesHandler(Resource):
    def __init__(self, ss : StudentServiceInterface) -> None:
        super().__init__()
        self.__ss : StudentServiceInterface = ss

    def get(self):
        c : CourseSection
        courses : Dict[str, List[CourseSection]] = self.__ss.get_student_courses(g.user)
        result : Dict[str, Any] = {}
        for k in courses:
            result[k] = [c.view() for c in courses[k]]

        return result


class StudentNotificationHandler(Resource):
    def __init__(self, ss : StudentServiceInterface) -> None:
        super().__init__()
        self.__ss : StudentServiceInterface = ss

    def get(self):
        n : Notification
        return [n.view() for n in self.__ss.get_student_notifications(g.user.id)]


class StudentRestrictionHandler(Resource):
    def __init__(self) -> None:
        super().__init__()

    def get(self):
        r : Restriction
        return [r.message for r in g.user.restrictions]

def register(api : Api, ss : StudentServiceInterface):
    api.add_resource(StudentCoursesHandler, "/api/student/courses", resource_class_kwargs={'ss': ss})
    api.add_resource(StudentNotificationHandler, "/api/student/notifications", resource_class_kwargs={'ss': ss})
    api.add_resource(StudentRestrictionHandler, "/api/student/restrictions")
