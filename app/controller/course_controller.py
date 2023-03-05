from typing import Dict, List

from flask import Blueprint
from flask import g
from flask import render_template
from flask import redirect
from flask import request
from flask import session
from flask import url_for
from sqlalchemy import select
from sqlalchemy.sql.expression import Select

from db import db
from form.course_search import CourseSearch
from model.course import CourseSection
from model.notification import Notification
from model.user import Student
from service.entity_manager import EntityManager
from service.registration_service import RegistrationService
from service.requirement_checker import create_registration_requirements_chain

bp : Blueprint = Blueprint('course', __name__, url_prefix='/course')
em : EntityManager = EntityManager(db)
rs : RegistrationService = RegistrationService(em, create_registration_requirements_chain())

@bp.before_app_request
def load_logged_in_user():
    g.user = em.get_by_id(Student, 5)

@bp.route('', methods=(['GET', 'POST']))
def search():
    courses : List[CourseSection] = []
    form : CourseSearch = CourseSearch(request.form)

    if request.method == "POST" and form.validate():
        stmt : Select = select(CourseSection).where(CourseSection.course_id == form.course_id.data)
        courses = em.get_by_criteria(stmt)

    return render_template('course/search.html', courses=courses, form=form)

@bp.route('/<int:id>', methods=(['GET', 'POST']))
def view(id : int):
    course : CourseSection = em.get_by_id(CourseSection, id)
    course_notifications : List[Notification] = []

    if request.method == "POST":
        if request.form.get("register") == "register":
            notification : Notification = rs.register(g.user.id, id)
            course_notifications.append(notification)
        elif request.form.get("drop") == "drop":
            pass

    return render_template('course/view.html', course=course, notifications=course_notifications)

@bp.route('/pending/<int:id>', methods=(['POST']))
def pending(id : int):
    rs.register_pending(g.user.id, id)

    return redirect(url_for("student.courses"))

@bp.route('/tentative/<int:id>', methods=(['POST']))
def tentative(id : int):
    rs.register_pending(g.user.id, id)

    return redirect(url_for("student.courses"))
