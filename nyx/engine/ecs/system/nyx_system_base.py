from abc import ABC
from nyx.engine.ecs.nyx_entity_manager import NyxEntityManager


class NyxSystem(ABC):
    def __init__(self, ecs: NyxEntityManager):
        self.ecs = ecs
