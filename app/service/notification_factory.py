from abc import ABC, abstractmethod
from typing import Any, Dict

from model.notification import BasicNotification, CoursePendingNotification, CourseTentativeNotification, Notification

class NotificationCreator(ABC):
    @abstractmethod
    def factory_method(self, data : Dict[str, Any]) -> Notification:
        pass

class BasicNotificationCreator(NotificationCreator):
    def factory_method(self, data : Dict[str, Any]) -> Notification:
        return BasicNotification(msg=data["msg"], type="info")

class CoursePendingNotificationCreator(NotificationCreator):
    def factory_method(self, data: Dict[str, Any]) -> Notification:
        return CoursePendingNotification(msg=data['msg'], type=data['type'], course_id=data['course_id'])

class CourseTentativeNotificationCreator(NotificationCreator):
    def factory_method(self, data: Dict[str, Any]) -> Notification:
        return CourseTentativeNotification(msg=data['msg'], type=data['type'], course_id=data['course_id'])
