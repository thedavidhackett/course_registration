from abc import ABC, abstractmethod
from typing import Any, Dict

from model.notification import (BasicNotification, DialogNotification, DialogFormNotification, Notification)

class NotificationCreator(ABC):
    @abstractmethod
    def factory_method(self, data : Dict[str, Any]) -> Notification:
        pass

class BasicNotificationCreator(NotificationCreator):
    def factory_method(self, data : Dict[str, Any]) -> Notification:
        return BasicNotification(msg=data["msg"], type="info")

class DialogNotificationCreator(NotificationCreator):
    def factory_method(self, data: Dict[str, Any]) -> Notification:
        return DialogNotification(msg=data['msg'], type=data['type'], action=data['action'], data=data['data'], submit_text=data['submit_text'])

class DialogFormNotificationCreator(NotificationCreator):
    def factory_method(self, data: Dict[str, Any]) -> Notification:
        return DialogFormNotification(msg=data['msg'], type=data['type'], action=data['action'], data=data['data'], options=data['options'], value_name=data['value_name'], submit_text=data['submit_text'])
