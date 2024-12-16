from typing import Dict
from nyx.moirai_ecs.component.component_manager import ComponentManager
from nyx.moirai_ecs.component.transform_components import (
    PositionComponent,
    VelocityComponent,
)
from nyx.moirai_ecs.entity.moirai_entity_manager import MoiraiEntityManager
from nyx.moirai_ecs.system.base_systems import BaseSystem
from nyx.nyx_engine.nyx_engine import NyxEngine


class MovementSystem(BaseSystem):
    """Update an entity's position component as a function of its velocity and time."""

    def update(self):
        entity_reg = MoiraiEntityManager.entity_registry
        position_reg: Dict[int, PositionComponent] = (
            ComponentManager.component_registry["position"]
        )
        velocity_reg: Dict[int, VelocityComponent] = (
            ComponentManager.component_registry["velocity"]
        )
        update_time = NyxEngine.sec_per_game_loop

        for entity_id, velocity_component in velocity_reg.items():
            if entity_id in entity_reg and entity_id in position_reg:
                position_component = position_reg[entity_id]

                # Update the x coordinate in the component
                dx = velocity_component.x_vel * update_time
                position_component.x_pos += dx
                position_component.render_x_pos = round(position_component.x_pos)

                # Update the y coordinate in the component
                dy = velocity_component.y_vel * update_time
                position_component.y_pos += dy
                position_component.render_y_pos = round(position_component.y_pos)
