from nyx.ecs.component.components import GraphicComponent, TileSetComponent
from nyx.ecs.nyx_entity_manager import NyxEntity, NyxEntityManager
from nyx.ecs.system.nyx_system_base import NyxSystem


class TileSetSystem(NyxSystem):
    def __init__(self, manager: NyxEntityManager):
        super().init(manager=manager)

    def add_tile(self, entity: NyxEntity, graphic_comp: GraphicComponent, tile_id: int):
        """_summary_

        Args:
            entity (NyxEntity): The entity with the `TileSetComponent` that contains the tile list.
            graphic_comp (GraphicComponent): The tile to add to the tile list.
            tile_id (int): The unoccupied index position of th enew tile in the tile list.

        Raises:
            ValueError: _description_
        """
        tileset = self._get_tile_set_comp(entity)
        if tile_id in tileset.tiles:
            raise ValueError(f"Tile ID {tile_id} already exists in the TileSet.")
        tileset.tiles[tile_id] = graphic_comp

    def get_tile(self, entity: NyxEntity, tile_id: int) -> GraphicComponent:
        tileset = self._get_tile_set_comp(entity)
        self._validate_tile_id(tile_id, tileset)
        return tileset.tiles[tile_id]

    def update_tile(
        self, entity: NyxEntity, graphic_comp: GraphicComponent, tile_id: int
    ):
        tileset = entity.get_components().get("TileSetComponent")
        self._validate_tile_id(tile_id, tileset)
        tileset.tiles[tile_id] = entity

    def delete_tile(self, entity: NyxEntity, tile_id: int):
        tileset = entity.get_components().get("TileSetComponent")
        self._validate_tile_id(tile_id, tileset)

    def _get_tile_set_comp(self, entity: NyxEntity) -> TileSetComponent:
        tileset = entity.get_components().get("TileSetComponent")
        if tileset is None:
            raise ValueError(
                f"Entity <{entity.entity_id!r}> does not have a TileSetComponent."
            )
        return tileset

    def _validate_tile_id(self, tile_id: int, tileset: TileSetComponent):
        if tile_id not in tileset.tiles:
            raise ValueError(f"Tile ID {tile_id} does not exist in the TileSet.")
