import numpy as np
from nyx.ecs.component.tile_component import GraphicComponent, TransformComponent
from nyx.ecs.nyx_entity_manager import NyxEntityManager
from nyx.ecs.system.render_system import RenderSystem


if __name__ == "__main__":
    nyx_ecs = NyxEntityManager()
    renderer = RenderSystem(view_width=100, view_height=40)

    graphic_1 = np.random.randint(low=14, high=255, size=(16, 16), dtype=np.uint8)
    tile_1 = (
        nyx_ecs.create_entity("random-tile-colors")
        .add_component(TransformComponent(0, 0))
        .add_component(GraphicComponent(graphic_1))
    )
    graphic_2 = np.random.randint(low=14, high=255, size=(8, 8), dtype=np.uint8)
    tile_2 = (
        nyx_ecs.create_entity("random-tile-colors")
        .add_component(TransformComponent(50-4, 20-4))
        .add_component(GraphicComponent(graphic_2))
    )
    graphic_3 = np.random.randint(low=14, high=255, size=(32, 32), dtype=np.uint8)
    tile_3 = (
        nyx_ecs.create_entity("random-tile-colors")
        .add_component(TransformComponent(100 - 32, 40 - 32))
        .add_component(GraphicComponent(graphic_3))
    )

    renderer.render(nyx_ecs)
