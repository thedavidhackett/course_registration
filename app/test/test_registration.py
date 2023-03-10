from db import db, notifications
from model.registration import Registration
from service.entity_manager import EntityManager
from service.notification_factory import BasicNotificationCreator
from service.notification_service import NotificationService
from service.registration_service import RegistrationService
from service.requirement_checker import create_registration_requirements_chain, create_pending_requirements_chain, create_tentative_requirements_chain
from service.course_service import CourseService

em : EntityManager = EntityManager(db)
ns : NotificationService = NotificationService(notifications, BasicNotificationCreator())
rs : RegistrationService = RegistrationService(em, CourseService(em), ns, BasicNotificationCreator())


def test_register_student():
    notification, success = rs.register(create_registration_requirements_chain(), 1, 514101)
    assert notification.msg == f"You successfully registered for 514101 - Object Oriented Programming"

    registration : Registration = rs.get_registration_by_student_id_and_course_id(1, 514101)
    assert registration.status == 'registered'

def test_register_student_with_restriction():
    notification, success = rs.register(create_registration_requirements_chain(), 2, 514101)
    assert notification.msg == "You have an unpaid fee"

def test_register_student_with_full_course_load():
    notification, success = rs.register(create_registration_requirements_chain(), 3, 514101)
    assert notification.msg == "Adding this course would overload your schedule. Would you like to request permission?"

def test_register_student_instructor_consent_required():
    notification, success = rs.register(create_registration_requirements_chain(), 1, 512301)
    assert notification.msg == "This course requires instructor approval? Would you like to request it"

def test_register_student_prereqs_not_met():
    notification, success = rs.register(create_registration_requirements_chain(), 1, 514201)
    assert notification.msg == "You have not met the prereqs for this course"

def test_register_student_course_full():
    notification, success = rs.register(create_registration_requirements_chain(), 1, 514102)
    assert notification.msg == "This course is full, here are other sections"

def test_register_pending():
    rs.register(create_pending_requirements_chain(), 3, 514101)
    registration : Registration = rs.get_registration_by_student_id_and_course_id(3, 514101)
    assert registration.status == "pending"

def test_register_tentative():
    rs.register(create_tentative_requirements_chain(), 1, 512301)
    registration : Registration = rs.get_registration_by_student_id_and_course_id(1, 512301)
    assert registration.status == "tentative"

def test_register_lab_required():
    notification, success = rs.register(create_registration_requirements_chain(), 1, 513001)
    assert notification.msg == "This course requires a lab, please select one."

def test_register_with_lab():
    notification, success = rs.register(create_registration_requirements_chain(), 1, 513001, 5130001)
    assert notification.msg == f"You successfully registered for 513001 - Compliers"

    registration : Registration = rs.get_registration_by_student_id_and_course_id(1, 513001)
    assert registration.status == "registered"
    assert registration.lab_section_id == 5130001

def test_already_registered_for_class():
    notification, success = rs.register(create_registration_requirements_chain(), 3, 514102)
    assert notification.msg == "You are already registered for this class"

def test_drop_class():
    notification = rs.drop_class(1, 514101)
    assert notification.msg == "Course 514101 was successfully dropped"

def test_drop_class_not_registered():
    notification = rs.drop_class(1, 514102)
    assert notification.msg == "You are not enrolled in this course"
