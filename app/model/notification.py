from abc import ABC, abstractmethod
from bson.objectid import ObjectId
from typing import Any, Dict, Type

class Notification(ABC):
    def __init__(self, id : ObjectId, msg : str, type : str) -> None:
        super().__init__()
        self.id : str = str(id)
        self.msg : str = msg
        self.type : str = type

class InfoNotification(Notification):
    def __init__(self, id: ObjectId, msg: str, type: str) -> None:
        super().__init__(id, msg, type)

class WarningNotification(Notification):
    def __init__(self, id : ObjectId, msg: str, type: str) -> None:
        super().__init__(id, msg, type)

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
