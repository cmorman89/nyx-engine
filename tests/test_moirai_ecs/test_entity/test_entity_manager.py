
from nyx.moirai_ecs.entity.moirai_entity_manager import MoiraiEntityManager
from nyx.moirai_ecs.entity.nyx_entity import NyxEntity
from nyx.nyx_engine.nyx_engine import NyxEngine

def test_entity_manager_construction():
    """Test that the entity manager can be initialized."""
    assert isinstance(MoiraiEntityManager(NyxEngine()), MoiraiEntityManager)


def test_create_entities():
    """Test the creation of entities (create, add to reg, return)."""
    entity_fate_manager = MoiraiEntityManager(NyxEngine())
    entity_list = []

    for i in range(10):
        entity_list.append(entity_fate_manager.create_entity())

    for entity in entity_list:
        assert entity in entity_list


def test_reset_entity_registry():
    """Test clearing the entire entity registry"""
    entity_fate_manager = MoiraiEntityManager(NyxEngine())
    entity_list = []

    # Create the entitiies
    for i in range(10):
        entity_list.append(entity_fate_manager.create_entity())

    # Clear the registry
    entity_fate_manager.reset_entity_registry()

    # Get the cleared registry
    entity_manager_list = MoiraiEntityManager.entity_registry

    # Remove the entities
    for entity in entity_list:
        assert entity.entity_id not in entity_manager_list


def test_destroy_entity():
    """Test the destruction of entities."""
    entity_fate_manager = MoiraiEntityManager(NyxEngine())
    entity_fate_manager.reset_entity_registry()
    entity_list = []

    # Create the entities
    for i in range(10):
        entity_list.append(entity_fate_manager.create_entity())

    # Get the registry
    entity_manager_list = MoiraiEntityManager.entity_registry

    # Remove the entities
    for entity in entity_list:
        entity_fate_manager.destroy_entity(entity.entity_id)
        assert entity.entity_id not in entity_manager_list


def test_is_alive():
    """Test if an entity is present in the entity list."""
    entity_fate_manager = MoiraiEntityManager(NyxEngine())
    entity_fate_manager.reset_entity_registry()
    entity_fate_manager.create_entity()

    assert entity_fate_manager.is_alive(entity_fate_manager.create_entity().entity_id)
    assert not entity_fate_manager.is_alive(-1)


def test_get_entity():
    """Test getting a single, existing entity"""
    entity_fate_manager = MoiraiEntityManager(NyxEngine())
    entity_fate_manager.reset_entity_registry()

    assert isinstance(
        entity_fate_manager.get_entity(entity_fate_manager.create_entity().entity_id),
        NyxEntity,
    )


def test_get_all_entities():
    """Test getting all entities from the manager"""
    entity_fate_manager = MoiraiEntityManager(NyxEngine())
    entity_fate_manager.reset_entity_registry()
    entity_list = []

    # Create the entities
    for _ in range(10):
        entity_list.append(entity_fate_manager.create_entity())

    assert len(entity_fate_manager.get_all_entities()) == 10
