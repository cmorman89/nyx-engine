"""
Render System Module

Rendering system to take a GraphicalComponent and print it to the terminal.

Note:
    - Chars to use: [ █ , ▀ , ▄ ]
    - This will likely split into the basic rendering system that then feeds into the larger terminal graphics rendering api
    -   FPS  Target Processing Time per Frame (ms)
        1                             1000.00
        5                               200.00
        10                             100.00
        15                               66.66
        30                               33.33
"""

from nyx.moros_ecs.component.renderable_components import RenderableComponent
from nyx.nyx_engine.stores.component_store import ComponentStore
from nyx.moros_ecs.moros_entity_manager import MorosEntityManager
from nyx.moros_ecs.system.moros_system_base import MorosSystem


class AetherBridgeSystem(MorosSystem):
    """Responsible for collecting all renderable components and passing them to Aether for
    composition and prioritization."""

    def __init__(
        self,
        entity_manager: MorosEntityManager,
        component_store: ComponentStore,
    ):
        super().__init__(entity_manager)
        self.component_store = component_store

    def update(self):
        """Get all renderable components"""
        z_indexed_entities = {}
        entity_registry = self.entity_manager.get_all_entities()
        for entity_id, entity in entity_registry.items():
            priority = -1
            entity_dict = {entity_id: {}}
            for comp_name, comp_obj in self.component_store.get_all_components(
                entity
            ).items():
                if isinstance(comp_obj, RenderableComponent):
                    entity_dict[entity_id][comp_name] = comp_obj
                    if comp_name == "ZIndexComponent":
                        priority = comp_obj.z_index
            if len(entity_dict[entity_id]) > 0:
                if priority not in z_indexed_entities:
                    z_indexed_entities[priority] = {}
                z_indexed_entities[priority][entity_id] = entity_dict[entity_id]

        if len(z_indexed_entities) > 0:
            return z_indexed_entities


#     def render(self, clear_term: bool = True):
#         """Render the entity to the terminal."""
#         entity_manager = self.ecs
#         buffer = np.zeros((self.view_height, self.view_width), dtype=np.uint8)
#         self._initialize_terminal(clear_term=clear_term)
#         for entity in entity_manager.entities:
#             components = entity.get_components()
#             transform_comp = components.get("TransformComponent")
#             graphic_comp = components.get("GraphicComponent")

#             if transform_comp and graphic_comp:
#                 x, y = transform_comp.x, transform_comp.y
#                 graphic_array = np.repeat(graphic_comp.graphic_arr, 3, axis=1)

#                 h, w = graphic_array.shape

#                 buffer[y : y + h, x : x + w] = graphic_array
#             self._preframe_actions()
#             self._draw_buffer(buffer=buffer)

#     def _draw_buffer(self, buffer: np.ndarray):
#         # Generate an empty array of correct dtype and one extra column.
#         row, cols = buffer.shape
#         rasterized_buffer = np.empty((row, cols + 1), dtype=">U20")
#         # Fill the new column with new line chars.
#         rasterized_buffer[:, -1] = "\n"
#         # Map buffer of ints to pre-generated, ANSI-formatted strings.
#         rasterized_buffer[:, :-1] = self._ansi_table[buffer]
#         # Write to the terminal.
#         sys.stdout.write("".join(rasterized_buffer.ravel()) + "\033[0m\n")
#         sys.stdout.flush()
