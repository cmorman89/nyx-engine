from nyx.moros_ecs.entity.nyx_entity import NyxEntity


def test_entity_init():
    entity = NyxEntity("friendly-name")
    assert isinstance(entity, NyxEntity)
    assert entity.friendly_name == "friendly-name"


def test_unique_entity_id():
    """Test if each entity gets a unique ID"""
    id_list = []
    for _ in range(10):
        entity = NyxEntity()
        id_list.append(entity.entity_id)

    assert len(set(id_list)) == len(id_list)
