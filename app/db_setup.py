from datetime import time
import pymongo
from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from model.base import Base
from model.course import Course, CourseSection, TimeSlot
from model.registration import Registration
from model.restriction import FeeRestriction
from model.user import Student

db = create_engine("mysql+pymysql://course_registration:course_registration@localhost:3306/course_registration")
client = MongoClient(host='localhost',port=27017, username='root',password='pass', authSource="admin")
mongo_db = client.notification_db
notification = mongo_db.notification
notification.drop()
notification.insert_many([{"student_id": 1, "type": "restriction", "msg": "You have a restriction"},\
                          {"student_id": 5, "type": "info", "msg": "This is a notification about something"}])
print(notification.find_one({"student_id": 1}))
Base.metadata.drop_all(db)
Base.metadata.create_all(db)

with Session(db) as session:
    student1 = Student("David", "Hackett", "graduate")
    student2 = Student("Roger", "Restriction", "graduate")
    student3 = Student("Nanette", "Nocapacity", "graduate", 1)
    student4 = Student("James", "Fake", "graduate")
    student5 = Student("Foo", "Bar", "graduate")
    course1 = Course(id=51410, name="Object Oriented Programming",\
         description="A class about object oriented programming")
    course2 = Course(id=51230, name="User Interface and User Experience Design",\
                     description="A class about designing interfaces", consent_required=True)
    course3 = Course(id=51420, name="Advanced Object Oriented Programming", \
                     description="For students who took objected oriented programming and want to learn more")

    course3.add_pre_req(course1)

    session.add_all([course1, course2, course3, student1, student2, student3, student4, student5])
    session.commit()

    time_slot1 = TimeSlot("Monday", time(16, 10), time(18, 0))
    time_slot2 = TimeSlot("Wednesday", time(17, 30), time(20, 30))
    time_slot3 = TimeSlot("Thursday", time(17, 30), time(20, 30))
    time_slot4 = TimeSlot("Wednesday", time(16, 10), time(18, 0))

    course_section1 = CourseSection(section_id=1, capacity=30, course=course1, times=[time_slot1])
    course_section2 = CourseSection(section_id=1, capacity=30, course=course2, times=[time_slot2])
    course_section3 = CourseSection(section_id=1, capacity=30, course=course3, times=[time_slot3])
    course_section4 = CourseSection(section_id=2, capacity=1, course=course1, times=[time_slot4])
    restriction : FeeRestriction = FeeRestriction(2)
    session.add_all([course_section1, course_section2, course_section3, course_section4, restriction])
    session.commit()

    reg1 = Registration("registered", student3.id, course_section4.id)
    reg2 = Registration("registered", student5.id, course_section1.id)
    reg3 = Registration("pending", student5.id, course_section2.id)
    session.add_all([reg1, reg2, reg3])
    session.commit()

    me = session.get(Student, 1)

    course = session.get(CourseSection, 514201)

    print(me.view())
    print(course.view())
