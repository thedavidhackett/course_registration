from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import declared_attr, Mapped, mapped_column

from .base import ManagedEntity

class Permission(ManagedEntity):
    __id : Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)
    student_id : Mapped[int] = \
        mapped_column("student_id", ForeignKey('student.id'))
    course_id : Mapped[int] = \
            mapped_column("course_id", ForeignKey('course.id'))
    approver_id : Mapped[int] = \
            mapped_column("approver_id", ForeignKey('instructor.id'))
    _approved : Mapped[bool] = mapped_column("approved")
    type: Mapped[str] = mapped_column("type", String(100))
    __mapper_args__ = {"polymorphic_on": "type"}


    def __init__(self, student_id : int, course_id : int, approver_id : int, approved : bool = False) -> None:
        super().__init__()
        self.student_id : int = student_id
        self.course_id : int = course_id
        self.approver_id : int = approver_id
        self._approved : int = approved

    def check_for_approval(self, course_id : int, type : str) -> bool:
        if course_id != self.course_id:
            return False

        if type != self.type:
            return False

        return self._approved


class OverloadPermission(Permission):
    @declared_attr.directive
    def __tablename__(cls) -> Optional[str]:
        return None

    __mapper_args__ = {"polymorphic_identity": "overload_permission"}

    def __init__(self, student_id: int, course_id: int, approver_id: int, approved: bool = False) -> None:
        super().__init__(student_id, course_id, approver_id, approved)

class InstructorPermission(Permission):
    @declared_attr.directive
    def __tablename__(cls) -> Optional[str]:
        return None

    __mapper_args__ = {"polymorphic_identity": "instructor_permission"}

    def __init__(self, student_id: int, course_id: int, approver_id: int, approved: bool = False) -> None:
        super().__init__(student_id, course_id, approver_id, approved)
