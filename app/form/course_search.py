from wtforms import Form, IntegerField

class CourseSearch(Form):
    course_id = IntegerField("Course ID")
