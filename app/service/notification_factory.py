from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from bson.objectid import ObjectId

from model.notification import (BasicNotification, DialogNotification, DialogFormNotification, Notification)

class NotificationCreator(ABC):
    def get_obj_id(self, data : Dict[str, Any]) -> Optional[str]:
        obj_id : Optional[ObjectId] = data.get("_id")
        id : Optional[str] = None
        if obj_id:
            id = str(obj_id)

        return id

    @abstractmethod
    def factory_method(self, data : Dict[str, Any]) -> Notification:
        pass

class BasicNotificationCreator(NotificationCreator):
    def factory_method(self, data : Dict[str, Any]) -> Notification:
        return BasicNotification(msg=data["msg"], type="info", id = self.get_obj_id(data))

class DialogNotificationCreator(NotificationCreator):
    def factory_method(self, data: Dict[str, Any]) -> Notification:
        return DialogNotification(msg=data['msg'], type=data['type'], action=data['action'], data=data['data'], submit_text=data['submit_text'], id = self.get_obj_id(data))

class DialogFormNotificationCreator(NotificationCreator):
    def factory_method(self, data: Dict[str, Any]) -> Notification:
        return DialogFormNotification(msg=data['msg'], type=data['type'], action=data['action'], data=data['data'], options=data['options'], value_name=data['value_name'], submit_text=data['submit_text'], id = self.get_obj_id(data))
