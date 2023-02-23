import os

from flask import Flask
from sqlalchemy import create_engine
from db import db


app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
)

# a simple page that says hello
@app.route('/hello')
def hello():
    return 'Hello, World!'


app.run(host="0.0.0.0")
