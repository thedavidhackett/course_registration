from typing import Dict, List
from model.course import CourseSection
from service.entity_manager import EntityManager

from db import db

def test_get_course_details():
    expected : Dict[str, object] = {
        "id": 514101,
        "course": {
            "id": 51410,
            "name" : "Object Oriented Programming",
            "description": "A class about object oriented programming",
        },
        "times": [
            {"day": "Monday", "start_time": "9:00AM", "end_time": "10:00AM"}
        ]
    }

    em : EntityManager = EntityManager(db)
    course_section : CourseSection = em.get_by_id(CourseSection, 514101)
    assert expected == course_section.view()
