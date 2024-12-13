from abc import ABC


class BaseComponent(ABC):
    """Abstract base class of all components in NyxEngine."""


class RenderableComponent(BaseComponent, ABC):
    """Abstract base class of all components that can be rendered by HemeraTerm"""
