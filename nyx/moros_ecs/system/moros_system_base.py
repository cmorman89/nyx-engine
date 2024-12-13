from abc import ABC

from nyx.moros_ecs.moros_entity_manager import MorosEntityManager


class MorosSystem(ABC):
    def __init__(self, entity_manager: MorosEntityManager):
        self.entity_manager: MorosEntityManager = entity_manager
