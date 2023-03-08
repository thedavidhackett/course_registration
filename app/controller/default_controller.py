from typing import List

from flask import g
from flask_restful import Api, Resource, reqparse

from db import db
from db import notifications
from model.notification import Notification
from service.entity_manager import EntityManager
from service.student_service import StudentService, StudentServiceInterface
from service.notification_factory import BasicNotificationCreator, NotificationCreator

em = EntityManager(db)
ss : StudentServiceInterface = StudentService(em)
notification_creator : NotificationCreator = BasicNotificationCreator()


class GetUserHandler(Resource):
  def get(self):
    return g.user.view()

def register(api : Api) -> None:
  api.add_resource(GetUserHandler, "/api/get-user")
