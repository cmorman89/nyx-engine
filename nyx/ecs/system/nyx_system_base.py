from abc import ABC
from nyx.ecs.nyx_entity_manager import NyxEntityManager


class NyxSystem(ABC):
    def __init__(self, manager: NyxEntityManager):
        self.manager = manager
