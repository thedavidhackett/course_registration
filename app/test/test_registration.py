from typing import Dict, List
from model.course import CourseSection
from model.registration import Registration
from model.user import Student
from service.entity_manager import EntityManager
from service.registration_manager import RegistrationManager
from db import db

em : EntityManager = EntityManager(db)
rm : RegistrationManager = RegistrationManager(em)


def test_register_student():
    success : bool
    msg : str
    success, msg = rm.register(1, 514101)
    assert success

    registration : Registration = em.get_by_id(Registration, 1)
    assert registration.status == 'registered'


def test_register_student_with_restriction():
    assert False

def test_register_student_with_full_course_load():
    assert False

def test_register_student_instructor_consent_required():
    assert False

def test_register_student_prereqs_not_met():
    assert False

def test_register_student_course_full():
    assert False
