from typing import Dict, List

from db import db
from model.course import CourseSection
from model.user import Student
from service.entity_manager import EntityManager
from service.student_service import StudentService

em : EntityManager = EntityManager(db)
ss : StudentService = StudentService(em)

def test_get_student_details():
    expected : Dict[str, object] = {
        "id" : 1,
        "name" : "David Hackett",
        "level" : "graduate"
    }

    student : Student = em.get_by_id(Student, 1)
    assert expected == student.view()


def test_get_student_courses():
    student : Student = em.get_by_id(Student, 5)
    courses : Dict[str, List[CourseSection]] = ss.get_student_courses(student)
    registered_course : CourseSection = em.get_by_id(CourseSection, 514101)
    pending_course : CourseSection = em.get_by_id(CourseSection, 512301)

    assert registered_course in courses['registered']
    assert pending_course in courses['pending']
