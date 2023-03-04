from typing import List
from flask import Blueprint
from flask import flash
from flask import g
from flask import render_template
from flask import session

from db import db
from db import notifications
from model.user import Student
from model.notification import Notification
from model.notification import NotificationCreator
from model.notification import InfoNotificationCreator
from service.entity_manager import EntityManager

bp = Blueprint('default', __name__, url_prefix='/')
em = EntityManager(db)
notification_creator : NotificationCreator = InfoNotificationCreator()

@bp.before_app_request
def load_logged_in_user():
    g.user = em.get_by_id(Student, 5)


@bp.route('/', methods=(['GET']))
def home():
    msgs : List[Notification] = [notification_creator.factory_method(data)\
                            for data in notifications.find({"student_id": 5, "type": "info"})]

    return render_template('student/home.html', notifications=msgs)
