from typing import Any, Dict, List

from flask import Blueprint, g, render_template
from flask_restful import Api, Resource, reqparse

from db import db
from model.course import CourseSection
from model.notification import Notification
from service.entity_manager import EntityManager
from service.notification_service import NotificationServiceInterface

class NotificationHandler(Resource):
    def __init__(self, ns : NotificationServiceInterface) -> None:
        super().__init__()
        self.__ns : NotificationServiceInterface = ns

    def delete(self, id : str):
        self.__ns.delete_notification(id)

def register(api : Api, ns : NotificationServiceInterface):
    api.add_resource(NotificationHandler, "/api/notifications/<string:id>", resource_class_kwargs={'ns': ns})
