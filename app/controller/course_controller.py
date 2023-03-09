from typing import Any, Dict, List

from flask import Blueprint, g,render_template, redirect, request, url_for
from flask_restful import Api, Resource, reqparse

from db import db
from form.course_search import CourseSearch
from model.course import CourseSection
from model.notification import Notification
from service.course_service import CourseService, CourseServiceInterface
from service.entity_manager import EntityManager
from service.notification_factory import BasicNotificationCreator
from service.registration_service import RegistrationService, RegistrationServiceInterface
from service.requirement_checker import create_registration_requirements_chain
from service.student_service import StudentService, StudentServiceInterface


class CourseSectionViewHandler(Resource):
    def __init__(self, cs : CourseServiceInterface) -> None:
        super().__init__()
        self.__cs : CourseServiceInterface = cs

    def get(self, id : int):
        course : CourseSection = self.__cs.get_course_section_by_id(id)
        result : Dict[str, Any] = course.view()
        result['enrolled'] = g.user.is_enrolled_in_course(id)
        return result

class CourseSearchHandler(Resource):
    def __init__(self, cs : CourseServiceInterface) -> None:
        super().__init__()
        self.__cs : CourseServiceInterface = cs

    def get(self):
        courses : List[CourseSection] = self.__cs.search(course_id=request.args.get("course_id"))
        c : CourseSection
        return [c.view() for c in courses]


def register(api : Api, cs : CourseServiceInterface) -> None:
        api.add_resource(CourseSectionViewHandler, "/api/course-section/<int:id>", resource_class_kwargs={'cs': cs})
        api.add_resource(CourseSearchHandler, "/api/courses", resource_class_kwargs={'cs': cs})
