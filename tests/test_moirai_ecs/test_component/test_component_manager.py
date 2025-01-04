from nyx.moirai_ecs.component.component_manager import ComponentManager
from nyx.moirai_ecs.component.transform_components import (
    DimensionsComponent,
    PositionComponent,
    ZIndexComponent,
)


def test_component_manager_construction():
    """Test that the component manager can be constructed successfully."""
    assert isinstance(ComponentManager(), ComponentManager)


def test_add_component():
    """Test that a component can be added successfuly."""
    entity_id = 1
    component_manager = ComponentManager()
    component_manager.remove_entity(entity_id=entity_id)
    component = DimensionsComponent(10, 10)
    component_manager.add_component(
        entity_id=entity_id, component_name="dimensions", component=component
    )
    assert component in component_manager.component_registry["dimensions"].values()


def test_get_component():
    """Test fetching a given component for an entity."""
    entity_id = 1
    component_manager = ComponentManager()
    component_manager.remove_entity(entity_id=entity_id)
    component_name = "dimensions"
    component = DimensionsComponent(10, 10)
    component_manager.add_component(
        entity_id=entity_id, component_name=component_name, component=component
    )
    assert (
        component_manager.get_component(
            entity_id=entity_id, component_name=component_name
        )
        == component
    )


def test_update_component():
    """Test that a component can be added successfuly."""
    entity_id = 0
    component_manager = ComponentManager()
    component_manager.remove_entity(entity_id=entity_id)
    component_name = "dimensions"
    component = DimensionsComponent(10, 10)
    component_2 = DimensionsComponent(20, 20)
    component_manager.add_component(
        entity_id=entity_id, component_name=component_name, component=component
    )
    component_manager.update_component(
        entity_id=entity_id, component_name=component_name, component=component_2
    )
    assert component_2 in component_manager.component_registry[component_name].values()


def test_destroy_component():
    """Test removing a component from the registry."""
    entity_id = 0
    component_manager = ComponentManager()
    component_manager.remove_entity(entity_id=entity_id)
    component_name = "dimensions"
    component = DimensionsComponent(10, 10)
    component_manager.add_component(
        entity_id=entity_id, component_name=component_name, component=component
    )
    component_manager.destroy_component(
        entity_id=entity_id, component_name=component_name
    )

    assert component not in component_manager.component_registry[component_name].values()


def test_remove_entity():
    """Test removing all entity components"""
    entity_id = 1
    component_manager = ComponentManager()
    component_manager.remove_entity(entity_id=entity_id)
    component_name = "dimensions"
    component_name_2 = "position"
    component_name_3 = "z-index"
    component = DimensionsComponent(10, 10)
    component_2 = PositionComponent(5, 5)
    component_3 = ZIndexComponent(4)
    component_manager.add_component(
        entity_id=entity_id, component_name=component_name, component=component
    )
    component_manager.add_component(
        entity_id=entity_id, component_name=component_name_2, component=component_2
    )
    component_manager.add_component(
        entity_id=entity_id, component_name=component_name_3, component=component_3
    )

    component_manager.remove_entity(entity_id=entity_id)

    for sub_dict in component_manager.component_registry.values():
        assert entity_id not in sub_dict.keys()
