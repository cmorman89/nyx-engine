import time
import numpy as np
from nyx.ecs.component.components import GraphicComponent, TransformComponent
from nyx.ecs.nyx_entity_manager import NyxEntityManager
from nyx.ecs.system.render_system import RenderSystem

if __name__ == "__main__":
    nyx_ecs = NyxEntityManager()
    renderer = RenderSystem(view_width=100, view_height=40, manager=nyx_ecs)
    RenderSystem.clear_terminal()
    while True:
        graphic_1 = np.random.randint(low=196, high=201, size=(16, 16), dtype=np.uint8)
        tile_1 = (
            nyx_ecs.create_entity("random-tile-colors")
            .add_component(TransformComponent(0, 0))
            .add_component(GraphicComponent(graphic_1))
        )
        graphic_3 = np.random.randint(low=22, high=51, size=(32, 32), dtype=np.uint8)
        tile_3 = (
            nyx_ecs.create_entity("random-tile-colors")
            .add_component(TransformComponent(100 - 96, 40 - 32))
            .add_component(GraphicComponent(graphic_3))
        )
        graphic_2 = np.random.randint(low=196, high=225, size=(8, 8), dtype=np.uint8)
        tile_2 = (
            nyx_ecs.create_entity("random-tile-colors")
            .add_component(TransformComponent(50 - 12, 20 - 4))
            .add_component(GraphicComponent(graphic_2))
        )

        renderer.render(clear_term=False)
        print(nyx_ecs)
        print(type[tile_1])
        print("Unloading assets:")
        nyx_ecs.unload_entity(tile_1).unload_entity(tile_2).unload_entity(tile_3)
        print(nyx_ecs)
        time.sleep(0.1)
