from datetime import time
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from model.base import Base
from model.course import Course, CourseSection, TimeSlot
from model.registration import Registration
from model.user import Student

db = create_engine("mysql+pymysql://course_registration:course_registration@localhost:3306/course_registration")

Base.metadata.drop_all(db)
Base.metadata.create_all(db)

with Session(db) as session:
    student = Student("David", "Hackett", "graduate")
    course = Course(id=51410, name="Object Oriented Programming",\
         description="A class about object oriented programming")

    time_slot = TimeSlot("Monday", time(9, 0), time(10, 0))

    course_section = CourseSection(id=514101, capacity=30, course=course, times=[time_slot])

    session.add_all([course, course_section, student])
    session.commit()

    me = session.get(Student, 1)

    print(me.view())
