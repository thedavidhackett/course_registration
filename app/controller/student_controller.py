from typing import Dict, List

from flask import Blueprint
from flask import flash
from flask import g
from flask import render_template
from flask import session

from db import db
from db import notifications
from model.user import Student
from model.course import CourseSection
from model.notification import Notification
from model.notification import NotificationCreator
from model.notification import InfoNotificationCreator
from service.entity_manager import EntityManager
from service.student_service import StudentService

bp : Blueprint = Blueprint('student', __name__, url_prefix='/student')
em : EntityManager = EntityManager(db)
ss : StudentService = StudentService(em)
notification_creator : NotificationCreator = InfoNotificationCreator()

@bp.before_app_request
def load_logged_in_user():
    g.user = em.get_by_id(Student, 5)


@bp.route('/courses', methods=(['GET']))
def courses():
    courses : Dict[str, List[CourseSection]] = ss.get_student_courses(g.user)
    return render_template('student/courses.html', courses=courses)
