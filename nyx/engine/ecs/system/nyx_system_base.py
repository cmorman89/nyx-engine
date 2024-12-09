from abc import ABC

from nyx.engine.managers.nyx_entity_manager import NyxEntityManager


class NyxSystem(ABC):
    def __init__(self, entity_manager: NyxEntityManager):
        self.entity_manager: NyxEntityManager = entity_manager
