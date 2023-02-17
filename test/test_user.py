from typing import Dict, List
from model.user import Student
from service.entity_manager import EntityManager

from db import db

def test_get_student_details():
    expected : Dict[str, object] = {
        "id" : 1,
        "name" : "David Hackett",
        "level" : "graduate"
    }

    em : EntityManager = EntityManager(db)
    student : Student = em.get_by_id(Student, 1)
    assert expected == student.view()
