from datetime import time
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session
from model.base import Base
from model.course import Course, CourseSection, TimeSlot
from model.restriction import FeeRestriction
from model.user import Student

db = create_engine("mysql+pymysql://course_registration:course_registration@localhost:3306/course_registration")

Base.metadata.drop_all(db)
Base.metadata.create_all(db)

with Session(db) as session:
    student = Student("David", "Hackett", "graduate")
    student2 = Student("Roger", "Restriction", "graduate")
    student3 = Student("Nanette", "Nocapacity", "graduate", 0)
    course = Course(id=51410, name="Object Oriented Programming",\
         description="A class about object oriented programming")
    course2 = Course(id=51230, name="User Interface and User Experience Design",\
                     description="A class about designing interfaces", consent_required=True)


    time_slot = TimeSlot("Monday", time(16, 10), time(18, 0))
    time_slot2 = TimeSlot("Wednesday", time(17, 30), time(20, 30))

    session.add_all([course, course2, student, student2, student3])
    session.commit()

    course_section = CourseSection(id=514101, capacity=30, course=course, times=[time_slot])
    course_section2 = CourseSection(id=512301, capacity=30, course=course2, times=[time_slot2])
    restriction : FeeRestriction = FeeRestriction(2)
    session.add_all([course_section, course_section2, restriction])
    session.commit()

    me = session.get(Student, 1)

    stmt = select(CourseSection).where(CourseSection.course_id == 51410)
    cs : CourseSection
    for cs in session.scalars(stmt):
        print(cs.view())

    print(me.view())
