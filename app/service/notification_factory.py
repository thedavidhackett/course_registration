from abc import ABC, abstractmethod
from typing import Any, Dict

from model.notification import InfoNotification
from model.notification import Notification
from model.notification import WarningNotification

class NotificationCreator(ABC):
    @abstractmethod
    def factory_method(self, data : Dict[str, Any]) -> Notification:
        pass

class InfoNotificationCreator(ABC):
    def factory_method(self, data : Dict[str, Any]) -> Notification:
        return InfoNotification(id=data["_id"], msg=data["msg"], type="info")

class WarningNotificationCreator(ABC):
    def factory_method(self, data : Dict[str, Any]) -> Notification:
        return WarningNotification(id=data["_id"], msg=data["msg"], type="warning")
