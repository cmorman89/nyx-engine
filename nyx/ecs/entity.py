from uuid import UUID, uuid4


class Entity:
    def __init__(self):
        self._entity_id = uuid4()

    @property
    def entity_id(self) -> UUID:
        return self._entity_id
