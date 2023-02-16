from typing import Dict, List
from datetime import time
from model.course import CourseSection
from service import CourseService

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

    course_service : CourseService = CourseService(db)
    course_section : CourseSection = course_service.get_by_id(514101)
    assert expected == course_section.get_details()
