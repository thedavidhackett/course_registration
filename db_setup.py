from datetime import time
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from model.base import Base
from model.course import Course, CourseSection, TimeSlot
from model.registration import Registration
from model.user import Student

db = create_engine("sqlite:///instance/course_registration.db", echo=True)

Base.metadata.drop_all(db)
Base.metadata.create_all(db)

with Session(db) as session:
    student = Student(1, "David", "Hackett", "graduate")
    course = Course(id=51410, name="Object Oriented Programming",\
         description="A class about object oriented programming")

    time_slot = TimeSlot(1, "Monday", time(9, 0), time(10, 0))

    course_section = CourseSection(id=514101, capacity=30, course=course, times=[time_slot])

    registration : Registration = Registration(1, "registered")

    student.add_registration(registration)
    course_section.add_registration(registration)

    session.add_all([course, course_section, student])
    session.commit()

    me = session.get(Student, 1)

    print(me.view())
