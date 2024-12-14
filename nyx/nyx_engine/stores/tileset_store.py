"""
Tileset Store Module

This module keeps a registry of tile textures by their unique tile ID, as well as a mapping of
friendly names to tile IDs.
"""

from typing import Dict

import numpy as np


class TilesetStore:
    """Holds and peforms CRUD operations on a class-level registry/dict of tile textures referenced
    by their tile ID, as well as a mapping of friendly names to tile IDs.

    Attributes:
        next_tile_id (int): The next valid, available tile_id.
        tileset_textures (Dict[int, np.ndarray]): The class-level repository of tile textures keyed
            by their unique tile ID number.
        tileset_friendly_name_map (Dict[str, int]): The class-level mapping of currently tile
            friendly names to their tile ID numbers.
    """

    next_tile_id: int = 0
    tileset_textures: Dict[int, np.ndarray] = {}
    tileset_friendly_name_map: Dict[str, int] = {}

    @classmethod
    def reset_store(cls):
        """Reset the state of the `TileStore` class attributes responsible for referencing and
        storing tiles.
        """
        cls.tileset_textures.clear()
        cls.tileset_friendly_name_map.clear()
        cls.next_tile_id = 0

    def __init__(self, tileset_textures: Dict[int, np.ndarray] = None):
        """Initialize the tileset store with a prepopulated tileset to add to the registry, or empty
        dicts if not set.

        Args:
            tileset_textures (Dict[int, np.ndarray], optional): The prepopulated tileset dict to
                import. Defaults to None.
        """
        TilesetStore.tileset_textures: Dict[int, np.ndarray] = (
            tileset_textures if tileset_textures else {}
        )
        TilesetStore.tileset_friendly_name_map: Dict[str, int] = {}

    def create_tile(
        self,
        tile_texture: np.ndarray,
        tile_id: int = None,
        tile_friendly_name: str = None,
        overwrite: bool = False,
    ):
        """Create and add a new tile to the tileset.

        Args:
            tile_texture (np.ndarray): The 2D NumPy array holding the tile's graphic data.
            tile_id (int, optional): Unique tile ID for this tile. Defaults to None, which auto-
                generates a new value.
            tile_friendly_name (str, optional): The human-readable, friendly name of this tile.
                Defaults to None.
            overwrite (bool, optional): Boolean flag allowing or prohibiting overwriting a tile
                with the same tile ID. Defaults to False.
        """
        tile_id = self._validate_tile_id(tile_id=tile_id, overwrite=overwrite)
        tile_friendly_name = self._validate_tile_friendly_name(
            tile_id=tile_id, tile_friendly_name=tile_friendly_name, overwrite=overwrite
        )

        TilesetStore.tileset_textures[tile_id] = tile_texture
        TilesetStore.tileset_friendly_name_map[tile_friendly_name] = tile_id

    def _validate_tile_id(self, tile_id: int = None, overwrite: bool = False) -> int:
        """Check that the tile has a unique, valid ID if set, or provide one if not set.

        Args:
            tile_id (int, optional): The tile ID to validate. Defaults to None.
            overwrite (bool, optional): Boolean flag indicating if a duplicate ID is allowed.
                Defaults to False.

        Raises:
            KeyError: If attempting to register an existing tile ID.
            ValueError: If attempting to set a tile ID outside bounds (0-255).

        Returns:
            int: The valid tile ID.
        """
        if tile_id and isinstance(tile_id, int):
            if 0 <= tile_id <= 255:
                if not overwrite and tile_id in TilesetStore.tileset_textures.keys():
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
    ) -> str:
        """Check that the tile has a unique, valid friendly_id, or provide a generic one if it is
        not set.

        Args:
            tile_id (int, optional): The tile ID to validate. Defaults to None.
            tile_friendly_name (str, optional): The human-readable, friendly name of this tile.
                Defaults to None.
            overwrite (bool, optional): Boolean flag indicating if a duplicate ID is allowed.
                Defaults to False.

        Raises:
            KeyError: If attempting to set a duplicate friendly name.

        Returns:
            str: The valid tile friendly name.
        """
        if tile_friendly_name and isinstance(tile_friendly_name, str):
            if (
                not overwrite
                and tile_friendly_name in TilesetStore.tileset_friendly_name_map.keys()
            ):
                raise KeyError(
                    f'Error: tile_friendly_name="{tile_friendly_name} for tile_id="{tile_id}" already registered to TilesetStore.'
                )
        else:
            tile_friendly_name = f"untitled-{tile_id}"
        return tile_friendly_name
