from abc import ABC, abstractmethod
from bson.objectid import ObjectId
from pymongo.collection import Collection
from typing import Any, Dict, List

from model.notification import Notification
from service.notification_factory import NotificationCreator

class NotificationServiceInterface(ABC):
    @abstractmethod
    def get_student_notifications(self, student_id : int) -> List[Notification]:
        pass

    @abstractmethod
    def create_notification(self, data : Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def delete_notification(self, notification_id : str) -> None:
        pass

class NotificationService(NotificationServiceInterface):
    def __init__(self, db : Collection, factory : NotificationCreator) -> None:
        super().__init__()
        self.__db : Collection = db
        self.__factory : NotificationCreator = factory

    def get_student_notifications(self, student_id: int) -> List[Notification]:
        return [self.__factory.factory_method(n) for n in self.__db.find({"student_id" : student_id})]

    def create_notification(self, data: Dict[str, Any]) -> None:
        self.__db.insert_one(data)

    def delete_notification(self, notification_id: str) -> None:
        self.__db.delete_one({"_id": ObjectId(notification_id)})
