from flask_restful import Api, Resource

from service.notification_service import NotificationServiceInterface

class NotificationHandler(Resource):
    def __init__(self, ns : NotificationServiceInterface) -> None:
        super().__init__()
        self.__ns : NotificationServiceInterface = ns

    def delete(self, id : str):
        self.__ns.delete_notification(id)

def register(api : Api, ns : NotificationServiceInterface):
    api.add_resource(NotificationHandler, "/api/notifications/<string:id>", resource_class_kwargs={'ns': ns})
