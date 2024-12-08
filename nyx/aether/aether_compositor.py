from typing import Dict
from uuid import UUID

from nyx.engine.ecs.component.renderable_components import RenderableComponent


class AetherCompositor:
    def __init__(self):
        self.layers = {}

    def accept_entities(
        self, entities: Dict[int, Dict[UUID, Dict[str, RenderableComponent]]]
    ):
        self.layers = entities
