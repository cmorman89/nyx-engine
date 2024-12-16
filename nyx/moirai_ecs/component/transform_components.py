"""
Renderable Components Module

This module contains components that modify the position, size, rotation, etc. of the entities that
can be rendered by Aether.
"""

from nyx.moirai_ecs.component.base_components import RenderableComponent


class ZIndexComponent(RenderableComponent):
    """Defines the layer prioritization (higher = higher priority)"""

    def __init__(self, z_index: int):
        self.z_index: int = z_index


class DimensionsComponent(RenderableComponent):
    def __init__(self, height: int, width: int):
        """Creates height, width bounds for an entity."""
        self.height = height
        self.width = width


class PositionComponenta(RenderableComponent):
    """Position of the the (0,0) origin of the entity within the frame."""

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
