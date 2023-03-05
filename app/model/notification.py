from abc import ABC

class Notification(ABC):
    def __init__(self, msg : str, type : str) -> None:
        super().__init__()
        self.msg : str = msg
        self.type : str = type

class BasicNotification(Notification):
    def __init__(self, msg: str, type: str) -> None:
        super().__init__(msg, type)

class CoursePendingNotification(Notification):
    def __init__(self, msg: str, type: str, course_id : int) -> None:
        super().__init__(msg, type)
        self.course_id : int = course_id

class CourseTentativeNotification(Notification):
    def __init__(self, msg: str, type: str, course_id : int) -> None:
        super().__init__(msg, type)
        self.course_id : int = course_id
