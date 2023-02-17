from typing import Tuple
from .entity_manager import EntityManager

class RegistrationManager:
    def __init__(self, em : EntityManager) -> None:
        self.__em : EntityManager = em


    def register(self, student_id : int, course_id : int) -> Tuple[bool, str]:
        return False, ""
