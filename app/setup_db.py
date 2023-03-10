from datetime import time

from sqlalchemy.orm import Session
from db import db, notifications
from model.base import Base
from model.course import Course, CourseSection, Department, LabSection, TimeSlot
from model.registration import Registration
from model.restriction import FeeRestriction, Restriction
from model.user import Instructor, Professor, Student
from service.notification_service import NotificationService
from service.notification_factory import BasicNotificationCreator

notifications.drop()
notifications.insert_many([{"student_id": 5, "type": "info", "msg": "Course registration closes in 3 days"},\
                          {"student_id": 5, "type": "info", "msg": "Please schedule a meeting with your advisor"}])

ns = NotificationService(notifications, BasicNotificationCreator())

notes = ns.get_student_notifications(5)


Base.metadata.drop_all(db)
Base.metadata.create_all(db)

with Session(db) as session:
    instructor1 = Professor("Bob", "Martin")
    instructor2 = Instructor("Jim", "Computers")
    instructor3 = Professor("Bill", "English")
    instructor4 = Instructor("John", "Irish")
    session.add_all([instructor1, instructor2, instructor3, instructor4])
    session.commit()

    department1 = Department("Computer Science", 1)
    department2 = Department("English", 3)

    session.add_all([department1, department2])
    session.commit()

    student1 = Student("David", "Hackett", "graduate")
    student2 = Student("Roger", "Restriction", "graduate")
    student3 = Student("Nanette", "Nocapacity", "graduate", 1)
    student4 = Student("James", "Fake", "graduate")
    student5 = Student("Foo", "Bar", "graduate")
    course1 = Course(id=51410, name="Object Oriented Programming",\
         description="A class about object oriented programming", department_id=1, instructor_id=1)
    course2 = Course(id=51230, name="User Interface and User Experience Design",\
                     description="A class about designing interfaces", department_id=1, instructor_id=2, consent_required=True)
    course3 = Course(id=51420, name="Advanced Object Oriented Programming", \
                     description="For students who took objected oriented programming and want to learn more", department_id=1, instructor_id=1)

    course4 = Course(id=51300, name="Compliers", description="A course on compliers", department_id=1, instructor_id=1, lab_required=True)
    course5 = Course(id=41000, name="Ulysses", description="Read the book", department_id=2, instructor_id=4)


    course3.add_pre_req(course1)

    session.add_all([course1, course2, course3, course4, student1, student2, student3, student4, student5])
    session.commit()

    time_slot1 = TimeSlot("Monday", time(16, 10), time(18, 0))
    time_slot2 = TimeSlot("Wednesday", time(17, 30), time(20, 30))
    time_slot3 = TimeSlot("Thursday", time(17, 30), time(20, 30))
    time_slot4 = TimeSlot("Wednesday", time(16, 10), time(18, 0))
    time_slot5 = TimeSlot("Tuesday", time(17,30), time(20,30))
    time_slot6 = TimeSlot("Friday", time(12,0), time(13,0))
    time_slot7 = TimeSlot("Friday", time(12,0), time(13,0))
    time_slot8 = TimeSlot("Monday", time(12,0), time(15,0))

    session.add_all([time_slot1, time_slot2, time_slot3, time_slot4, time_slot5, time_slot6, time_slot7, time_slot8])
    session.commit()

    course_section1 = CourseSection(section_id=1, capacity=30, course=course1, times=[time_slot1])
    course_section2 = CourseSection(section_id=1, capacity=30, course=course2, times=[time_slot2])
    course_section3 = CourseSection(section_id=1, capacity=30, course=course3, times=[time_slot3])
    course_section4 = CourseSection(section_id=2, capacity=1, course=course1, times=[time_slot4])
    course_section5 = CourseSection(section_id=1, capacity=30, course=course4, times=[time_slot5])
    course_section6 = CourseSection(section_id=1, capacity=10, course=course5, times=[time_slot8])
    lab_section1 = LabSection(section_id=1, capacity=15, course=course4, times=[time_slot6])
    lab_section2 = LabSection(section_id=2, capacity=15, course=course4, times=[time_slot7])

    restriction : FeeRestriction = FeeRestriction(student2.id)
    session.add_all([course_section1, course_section2, course_section3, course_section4,\
                      course_section5, course_section6, lab_section1, lab_section2, restriction])
    session.commit()

    reg1 = Registration("registered", student3.id, course_section4.id)
    reg2 = Registration("registered", student5.id, course_section1.id)
    session.add_all([reg1, reg2])
    session.commit()

    me = session.get(Student, 1)
    roger = session.get(Student, student2.id)


    res = session.get(Restriction, 1)


    course = session.get(CourseSection, 514201)
    lab = session.get(LabSection, 5130001)
