from abc import ABC

from nyx.engine.ecs.entity.nyx_entity_manager import NyxEntityManager


class NyxSystem(ABC):
    def __init__(self, entity_manager: NyxEntityManager):
        self.entity_manager: NyxEntityManager = entity_manager
