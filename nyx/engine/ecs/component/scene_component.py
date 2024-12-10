from nyx.engine.ecs.component.renderable_components import RenderableComponent


class SceneComponent(RenderableComponent):
    """Signify entity as a high level/top level component"""

    def __init__(self, friendly_name: str):
        self.friendly_name = friendly_name
