import numpy as np
from nyx.moirai_ecs.component.base_components import NyxComponent


class TextureComponent(NyxComponent):
    """Define a texture for an entity"""

    def __init__(self, texture: np.ndarray):
        if texture.dtype != np.uint8:
            raise ValueError("NumPy array must be of type 'uint8'.")
        self.texture = texture
