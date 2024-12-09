from typing import Dict

import numpy as np


class TilesetStore:
    next_tile_id = 0

    def __init__(self, tileset_textures: Dict[int, np.ndarray] = None):
        self.tileset_textures: Dict[int, np.ndarray] = (
            tileset_textures if tileset_textures else {}
        )
        self.tileset_friendly_name_map: Dict[str, int] = {}

    def create_tile(
        self,
        tile_texture: np.ndarray,
        tile_id: int = None,
        tile_friendly_name: str = None,
        overwrite: bool = False,
    ):
        tile_id = self._validate_tile_id(tile_id=tile_id, overwrite=overwrite)
        tile_friendly_name = self._validate_tile_friendly_name(
            tile_id=tile_id, tile_friendly_name=tile_friendly_name, overwrite=overwrite
        )

        self.tileset_textures[tile_id] = tile_texture
        self.tileset_friendly_name_map[tile_friendly_name] = tile_id

    def _validate_tile_id(self, tile_id: int = None, overwrite: bool = False):
        if tile_id and isinstance(tile_id, int):
            if 0 <= tile_id <= 255:
                if not overwrite and tile_id in self.tileset_textures.keys():
                    raise KeyError(
                        f'Error: tile_id="{tile_id}" already registered to TilesetStore.'
                    )
            else:
                raise ValueError(
                    f'Out of bounds: tile_id="{tile_id}" must be bewteen 0 and 255.'
                )
        else:
            tile_id = TilesetStore.next_tile_id
            TilesetStore.next_tile_id += 1
        return tile_id

    def _validate_tile_friendly_name(
        self, tile_id: int, tile_friendly_name: str = None, overwrite: bool = False
    ):
        if tile_friendly_name and isinstance(tile_friendly_name, str):
            if (
                not overwrite
                and tile_friendly_name in self.tileset_friendly_name_map.keys()
            ):
                raise KeyError(
                    f'Error: tile_friendly_name="{tile_friendly_name} for tile_id="{tile_id}" already registered to TilesetStore.'
                )
        else:
            tile_friendly_name = f"untitled-{tile_id}"
        return tile_friendly_name
