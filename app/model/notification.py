from abc import ABC
from typing import Any, Dict, List, Optional

class Notification(ABC):
    def __init__(self, msg : str, type : str, id : Optional[str]= None) -> None:
        super().__init__()
        self.id : Optional[str] = id
        self.msg : str = msg
        self.type : str = type

    def view(self) -> Dict[str, object]:
        return {"msg": self.msg, "type": self.type , "id": self.id}

class BasicNotification(Notification):
    def __init__(self, msg: str, type: str, id : Optional[str] = None) -> None:
        super().__init__(msg, type, id)

class DialogNotification(Notification):
    def __init__(self, msg: str, type: str, submit_text : str, action : str, data : Dict[str, Any], id : Optional[str] = None) -> None:
        super().__init__(msg, type, id)
        self.submit_text : str = submit_text
        self.action : str = action
        self.data : Dict[str, Any] = data

    def view(self) -> Dict[str, object]:
        result : Dict[str, object] = super().view()
        result['submit_text'] = self.submit_text
        result['action'] = self.action
        result['data'] = self.data

        return result

class DialogFormNotification(DialogNotification):
    def __init__(self, msg: str, type: str, submit_text: str, action: str, data: Dict[str, Any], value_name: str, options : List[Dict[str, Any]], id : Optional[str] = None) -> None:
        super().__init__(msg, type, submit_text, action, data, id)
        self.value_name = value_name
        self.options = options

    def view(self) -> Dict[str, object]:
        result : Dict[str, object] = super().view()
        result['value_name'] = self.value_name
        result['options'] = self.options

        return result
