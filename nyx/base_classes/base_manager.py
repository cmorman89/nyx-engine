from abc import ABC

from nyx.aether_renderer.aether_dimensions import AetherDimensions
from nyx.nyx_engine.nyx_engine import NyxEngine


class BaseManager:
    @property
    def engine(self) -> NyxEngine:
        return NyxEngine()

    @property
    def dimensions(self) -> AetherDimensions:
        return self.engine.aether_dimensions
