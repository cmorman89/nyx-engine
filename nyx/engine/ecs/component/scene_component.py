from nyx.engine.ecs.component.nyx_component import NyxComponent


class SceneComponent(NyxComponent):
    """Signify entity as a high level/top level component"""

    def __init__(self, friendly_name: str):
        self.friendly_name = friendly_name
