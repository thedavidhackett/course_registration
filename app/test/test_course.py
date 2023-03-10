from typing import Dict, List

from db import db
from model.course import CourseSection
from service.entity_manager import EntityManager
from service.course_service import CourseService

em : EntityManager = EntityManager(db)
cs : CourseService = CourseService(em)

def test_get_course_details():
    expected : Dict[str, object] = {
        "id": 514101,
        "course": {
            "id": 51410,
            "name" : "Object Oriented Programming",
            "description": "A class about object oriented programming",
        },
        "times": [
            {"day": "Monday", "start_time": "4:10PM", "end_time": "6:00PM"}
        ],
    }

    em : EntityManager = EntityManager(db)
    course_section : CourseSection = em.get_by_id(CourseSection, 514101)
    assert expected == course_section.view()


def test_course_search_just_id():
    course_section1 : CourseSection = cs.get_course_section_by_id(514101)
    course_section2 : CourseSection = cs.get_course_section_by_id(514102)

    courses : List[CourseSection] = cs.search(51410)
    cs_ids = [c.id for c in courses]
    assert course_section1.id in cs_ids
    assert course_section2.id in cs_ids


def test_course_search_just_department():
    course_section : CourseSection = cs.get_course_section_by_id(410001)

    courses : List[CourseSection] = cs.search(None, 2)
    cs_ids = [c.id for c in courses]
    assert course_section.id in cs_ids


def test_course_search_both_id_department():
    course_section : CourseSection = cs.get_course_section_by_id(410001)

    courses : List[CourseSection] = cs.search(None, 2)
    cs_ids = [c.id for c in courses]
    assert course_section.id in cs_ids
