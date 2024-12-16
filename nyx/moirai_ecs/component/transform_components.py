"""
Renderable Components Module

This module contains components that modify the position, size, rotation, etc. of the entities that
can be rendered by Aether.
"""

from nyx.moirai_ecs.component.base_components import NyxComponent


class ZIndexComponent(NyxComponent):
    """Define the layer prioritization (higher = higher priority)"""
    def __init__(self, z_index: int):
        self.z_index: int = z_index


class DimensionsComponent(NyxComponent):
    """Create height, width bounds for an entity."""
    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width


class PositionComponent(NyxComponent):
    """Position of the the (0,0) origin of the entity within the frame."""
    def __init__(self, x_pos: int = 0, y_pos: int = 0):
        self.x_pos = x_pos
        self.y_pos = y_pos

class VelocityComponent(NyxComponent):
    """Define the current speed of the component in pixels per refresh."""
    def __init__(self, x_vel: int = 0, y_vel: int = 0):
        self.x_vel = x_vel
        self.y_vel = y_vel