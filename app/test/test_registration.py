from db import db
from model.registration import Registration
from service.entity_manager import EntityManager
from service.notification_factory import BasicNotificationCreator
from service.registration_service import RegistrationService
from service.requirement_checker import create_registration_requirements_chain

em : EntityManager = EntityManager(db)
rs : RegistrationService = RegistrationService(em, create_registration_requirements_chain(), BasicNotificationCreator())


def test_register_student():
    notification = rs.register(1, 514101)
    assert notification.msg == f"You successfully registered for 514101 - Object Oriented Programming"

    registration : Registration = rs.get_registration_by_student_id_and_course_id(1, 514101)
    assert registration.status == 'registered'

def test_register_student_with_restriction():
    notification = rs.register(2, 514101)
    assert notification.msg == "You have an unpaid fee"

def test_register_student_with_full_course_load():
    notification = rs.register(3, 514101)
    assert notification.msg == "Adding this course would overload your schedule. Would you like to request permission?"

def test_register_student_instructor_consent_required():
    msg : str
    notification = rs.register(1, 512301)
    assert notification.msg == "This course requires instructor approval? Would you like to request it"

def test_register_student_prereqs_not_met():
    notification = rs.register(1, 514201)
    assert notification.msg == "You have not met the prereqs for this course"

def test_register_student_course_full():
    notification = rs.register(1, 514102)
    assert notification.msg == "This course is full"

def test_register_pending():
    rs.register_pending(3, 514101)
    registration : Registration = rs.get_registration_by_student_id_and_course_id(3, 514101)
    assert registration.status == "pending"

def test_register_tentative():
    rs.register_tentative(1, 512301)
    registration : Registration = rs.get_registration_by_student_id_and_course_id(1, 512301)
    assert registration.status == "tentative"

def test_drop_class():
    notification = rs.drop_class(1, 514101)
    assert notification.msg == "Course 514101 was successfully dropped"

def test_drop_class_not_registered():
    notification = rs.drop_class(1, 514102)
    assert notification.msg == "You are not enrolled in this course"
