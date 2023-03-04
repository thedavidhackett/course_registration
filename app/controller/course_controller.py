from typing import Dict, List

from flask import Blueprint
from flask import g
from flask import render_template
from flask import request
from flask import session
from sqlalchemy import select
from sqlalchemy.sql.expression import Select

from db import db
from form.course_search import CourseSearch
from model.user import Student
from model.course import CourseSection
from service.entity_manager import EntityManager

bp : Blueprint = Blueprint('course', __name__, url_prefix='/course')
em : EntityManager = EntityManager(db)

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
    return render_template('course/view.html', course=course)
