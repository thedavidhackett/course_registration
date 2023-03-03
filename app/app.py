import os
from flask import Flask
from controller import course_controller
from controller import default_controller
from controller import student_controller

def create_app(testing=False):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if testing:
        app.config.update({'TESTING': True})

    app.register_blueprint(default_controller.bp)
    app.register_blueprint(student_controller.bp)
    app.register_blueprint(course_controller.bp)


    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0")
