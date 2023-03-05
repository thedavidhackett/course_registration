from typing import List

from flask import Blueprint, g,render_template, redirect, request, url_for

from db import db
from form.course_search import CourseSearch
from model.course import CourseSection
from model.notification import Notification
from service.course_service import CourseService, CourseServiceInterface
from service.entity_manager import EntityManager
from service.notification_factory import BasicNotificationCreator
from service.registration_service import RegistrationService, RegistrationServiceInterface
from service.requirement_checker import create_registration_requirements_chain
from service.student_service import StudentService, StudentServiceInterface

bp : Blueprint = Blueprint('course', __name__, url_prefix='/course')
em : EntityManager = EntityManager(db)
ss : StudentServiceInterface = StudentService(em)
rs : RegistrationServiceInterface = RegistrationService(em, create_registration_requirements_chain(), BasicNotificationCreator())
cs : CourseServiceInterface = CourseService(em)

@bp.before_app_request
def load_logged_in_user():
    g.user = ss.get_student_by_id(5)

@bp.route('', methods=(['GET', 'POST']))
def search():
    courses : List[CourseSection] = []
    form : CourseSearch = CourseSearch(request.form)

    if request.method == "POST" and form.validate():
        courses = cs.search(course_id=form.course_id.data)

    return render_template('course/search.html', courses=courses, form=form)

@bp.route('/<int:id>', methods=(['GET', 'POST']))
def view(id : int):
    course : CourseSection = em.get_by_id(CourseSection, id)
    course_notifications : List[Notification] = []

    if request.method == "POST":
        if request.form.get("register") == "register":
            reg_notification : Notification = rs.register(g.user.id, id)
            course_notifications.append(reg_notification)
        elif request.form.get("drop") == "drop":
            drop_notification : Notification = rs.drop_class(g.user.id, id)
            course_notifications.append(drop_notification)

    return render_template('course/view.html', course=course, notifications=course_notifications)

@bp.route('/pending/<int:id>', methods=(['POST']))
def pending(id : int):
    rs.register_pending(g.user.id, id)

    return redirect(url_for("student.courses"))

@bp.route('/tentative/<int:id>', methods=(['POST']))
def tentative(id : int):
    rs.register_pending(g.user.id, id)

    return redirect(url_for("student.courses"))
