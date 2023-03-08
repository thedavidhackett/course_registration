from typing import Any, Dict, List

from flask import Blueprint, g, render_template
from flask_restful import Api, Resource, reqparse

from db import db
from model.course import CourseSection
from service.entity_manager import EntityManager
from service.notification_factory import BasicNotificationCreator, NotificationCreator
from service.student_service import StudentService, StudentServiceInterface

bp : Blueprint = Blueprint('student', __name__, url_prefix='/student')
em : EntityManager = EntityManager(db)
ss : StudentServiceInterface = StudentService(em)
notification_creator : NotificationCreator = BasicNotificationCreator()



class StudentCoursesHandler(Resource):
    def __init__(self, ss : StudentServiceInterface) -> None:
        super().__init__()
        self.__ss = ss

    def get(self):
        c : CourseSection
        courses : Dict[str, List[CourseSection]] = self.__ss.get_student_courses(g.user)
        result : Dict[str, Any] = {}
        for k in courses:
            result[k] = [c.view() for c in courses[k]]

        return result


def register(api : Api, ss : StudentServiceInterface):
    api.add_resource(StudentCoursesHandler, "/api/student/courses", resource_class_kwargs={'ss': ss})
