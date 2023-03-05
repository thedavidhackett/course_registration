from typing import List

from flask import Blueprint, g, render_template

from db import db
from db import notifications
from model.notification import Notification
from service.entity_manager import EntityManager
from service.student_service import StudentService, StudentServiceInterface
from service.notification_factory import BasicNotificationCreator, NotificationCreator

bp = Blueprint('default', __name__, url_prefix='/')
em = EntityManager(db)
ss : StudentServiceInterface = StudentService(em)
notification_creator : NotificationCreator = BasicNotificationCreator()

@bp.before_app_request
def load_logged_in_user():
    g.user = ss.get_student_by_id(5)


@bp.route('/', methods=(['GET']))
def home():
    msgs : List[Notification] = [notification_creator.factory_method(data)\
                            for data in notifications.find({"student_id": 5})]

    return render_template('student/home.html', notifications=msgs)
