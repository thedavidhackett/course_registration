import os
from flask import Flask

def create_app(testing=False):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if testing:
        app.config.update({'TESTING': True})

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0")
