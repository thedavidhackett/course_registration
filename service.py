from model.course import CourseSection
from sqlalchemy.orm import Session


class CourseService:
    def __init__(self, db) -> None:
        self.__db = db

    def get_by_id(self, id) -> CourseSection:
        course : CourseSection
        with Session(self.__db) as s:
            course = s.get(CourseSection, id)

        return course
