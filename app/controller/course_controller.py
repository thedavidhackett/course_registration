from typing import Any, Dict, List

from flask import g, request
from flask_restful import Api, Resource

from model.course import CourseSection, Department
from service.course_service import CourseServiceInterface


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
        courses : List[CourseSection] = self.__cs.search(course_id=request.args.get("course_id"), department_id=request.args.get("department_id"))
        c : CourseSection
        return [c.view() for c in courses]


class DepartmentsHandler(Resource):
    def __init__(self, cs : CourseServiceInterface) -> None:
        super().__init__()
        self.__cs : CourseServiceInterface = cs

    def get(self):
        departments : List[Department] = self.__cs.get_departments()
        d : Department
        return [d.view() for d in departments]


def register(api : Api, cs : CourseServiceInterface) -> None:
        api.add_resource(CourseSectionViewHandler, "/api/course-section/<int:id>", resource_class_kwargs={'cs': cs})
        api.add_resource(CourseSearchHandler, "/api/courses", resource_class_kwargs={'cs': cs})
        api.add_resource(DepartmentsHandler, "/api/departments", resource_class_kwargs={'cs': cs})
