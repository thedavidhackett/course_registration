import os

from flask import Flask, g, send_from_directory
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS

from db import db, notifications
from controller import course_controller, default_controller, registration_controller, notification_controller, student_controller
from service.course_service import CourseService
from service.student_service import StudentService
from service.entity_manager import EntityManager
from service.registration_service import RegistrationService
from service.notification_service import NotificationService
from service.notification_factory import BasicNotificationCreator
from service.requirement_checker import (create_registration_requirements_chain,
                                         create_pending_requirements_chain,
                                         create_tentative_requirements_chain)


def create_app(testing=False):
    app = Flask(__name__, static_url_path='', static_folder='frontend/build')
    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    if testing:
        app.config.update({'TESTING': True})

    CORS(app)
    api = Api(app)

    em = EntityManager(db)
    ns = NotificationService(notifications, BasicNotificationCreator())
    ss = StudentService(em, ns)
    cs = CourseService(em)
    rs = RegistrationService(em, cs, ns, BasicNotificationCreator())

    @app.before_request
    def load_logged_in_user():
        g.user = ss.get_student_by_id(5)

    @app.route("/", defaults={'path':''})
    def serve(path):
        return send_from_directory(app.static_folder,'index.html')

    default_controller.register(api)
    course_controller.register(api, cs)
    registration_controller.register(api, rs, rs, create_registration_requirements_chain(), create_pending_requirements_chain(), create_tentative_requirements_chain())
    student_controller.register(api, ss)
    notification_controller.register(api, ns)


    return app



if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0")
