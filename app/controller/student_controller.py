from typing import Dict, List

from flask import Blueprint, g, render_template

from db import db
from model.course import CourseSection
from service.entity_manager import EntityManager
from service.notification_factory import BasicNotificationCreator, NotificationCreator
from service.student_service import StudentService, StudentServiceInterface

bp : Blueprint = Blueprint('student', __name__, url_prefix='/student')
em : EntityManager = EntityManager(db)
ss : StudentServiceInterface = StudentService(em)
notification_creator : NotificationCreator = BasicNotificationCreator()

@bp.before_app_request
def load_logged_in_user():
    g.user = ss.get_student_by_id(5)

@bp.route('/courses', methods=(['GET']))
def courses():
    courses : Dict[str, List[CourseSection]] = ss.get_student_courses(g.user)
    return render_template('student/courses.html', courses=courses)
