from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import declared_attr, Mapped, mapped_column

from .base import ManagedEntity

class Restriction(ManagedEntity):
    __id : Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)
    student_id : Mapped[int] = \
        mapped_column("student_id", ForeignKey('student.id'))
    type: Mapped[str] = mapped_column("type", String(100))
    __mapper_args__ = {"polymorphic_on": "type"}

    def __init__(self, student_id : int) -> None:
        super().__init__()
        self.student_id = student_id

    @property
    def message(self) -> str:
        return "You have a restriction"

    def can_register(self) -> bool:
        return False

class FeeRestriction(Restriction):
    @declared_attr.directive
    def __tablename__(cls) -> Optional[str]:
        return None

    __mapper_args__ = {"polymorphic_identity": "fee_restriction"}

    def __init__(self, student_id: int) -> None:
        super().__init__(student_id)

    @property
    def message(self) -> str:
        return "You have an unpaid fee"
