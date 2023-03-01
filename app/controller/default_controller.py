from flask import Blueprint
from flask import g
from flask import render_template
from flask import session
from model.user import Student
from service.entity_manager import EntityManager
from db import db

bp = Blueprint('default', __name__, url_prefix='/')
em = EntityManager(db)

@bp.before_app_request
def load_logged_in_user():
    g.user = em.get_by_id(Student, 5)

@bp.route('/', methods=(['GET']))
def home():
    return render_template('student/home.html')
