from typing import Dict, List
from model.course import CourseSection
from model.registration import Registration
from model.user import Student
from service.entity_manager import EntityManager
from service.registration_service import RegistrationService
from service.requirement_checker import create_registration_requirements_chain
from db import db

em : EntityManager = EntityManager(db)
rs : RegistrationService = RegistrationService(em)
checker = create_registration_requirements_chain()


def test_register_student():
    msg : str
    msg = rs.register(1, 514101, checker)
    assert msg == "registered"

    registration : Registration = rs.get_registration_by_student_id_and_course_id(1, 514101)
    assert registration.status == 'registered'

def test_register_student_with_restriction():
    msg : str
    msg = rs.register(2, 514101, checker)
    assert msg == "You have an unpaid fee"

def test_register_student_with_full_course_load():
    msg : str
    msg = rs.register(3, 514101, checker)
    assert msg == "pending"

    registration : Registration = rs.get_registration_by_student_id_and_course_id(3, 514101)
    assert registration.status == 'pending'

def test_register_student_instructor_consent_required():
    msg : str
    msg = rs.register(1, 512301, checker)
    assert msg == "tentative"

    registration : Registration = rs.get_registration_by_student_id_and_course_id(1, 512301)
    assert registration.status == 'tentative'

def test_register_student_prereqs_not_met():
    assert False

def test_register_student_course_full():
    assert False
