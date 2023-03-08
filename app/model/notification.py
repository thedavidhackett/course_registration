from abc import ABC
from typing import Any, Dict, List

class Notification(ABC):
    def __init__(self, msg : str, type : str) -> None:
        super().__init__()
        self.msg : str = msg
        self.type : str = type

class BasicNotification(Notification):
    def __init__(self, msg: str, type: str) -> None:
        super().__init__(msg, type)

class DialogNotification(Notification):
    def __init__(self, msg: str, type: str, submit_text : str, action : str, data : Dict[str, Any]) -> None:
        super().__init__(msg, type)
        self.submit_test : str = submit_text
        self.action : int = action
        self.data : Dict[str, Any] = data

class DialogFormNotification(DialogNotification):
    def __init__(self, msg: str, type: str, submit_text: str, action: str, data: Dict[str, Any], value_name: str, options : List[Dict[str, Any]]) -> None:
        super().__init__(msg, type, submit_text, action, data)
        self.value_name = value_name
        self.options = options
