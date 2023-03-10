from abc import ABC, abstractmethod
from typing import Optional
from model.permission import Permission

class PermissionServiceInterface(ABC):
    @abstractmethod
    def get_permission_by_instructor_and_student_id(self, instructor_id: int, student_id : int) -> Optional[Permission]:
        pass

    @abstractmethod
    def create_overload_permission(self, student_id : int, course_id : int) -> None:
        pass

    @abstractmethod
    def create_instructor_permission(self, student_id : int, course_id : int) -> None:
        pass
