from sqlalchemy import create_engine

db = create_engine("mysql+pymysql://course_registration:course_registration@localhost:3306/course_registration")
