import os

from flask import Flask, g, send_from_directory
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS

from db import db
from controller import default_controller, student_controller
from service.student_service import StudentService
from service.entity_manager import EntityManager


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
    ss = StudentService(em)

    @app.before_request
    def load_logged_in_user():
        g.user = ss.get_student_by_id(5)

    @app.route("/", defaults={'path':''})
    def serve(path):
        return send_from_directory(app.static_folder,'index.html')

    default_controller.register(api)
    student_controller.register(api, ss)


    return app



if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0")
