import sys
import numpy as nd
from nyx.data.nyx_graphic_asset import NyxGraphicAsset
from nyx.engine.ecs.components.nyx_engine_component import NyxEngineComponent
from nyx.engine.ecs.components.sprite_component import Sprite
from nyx.engine.ecs.components.tilemap_component import TileMapComponent


def render(
    nyx_obj: NyxEngineComponent,
    origin_x: int = None,
    origin_y: int = None,
    rel_x: int = None,
    rel_y: int = None,
):
    up = 0
    down = 0
    left = 0
    right = 0
    if rel_x or rel_y:
        if rel_x is not None and rel_x > 0:
            down = rel_x
        elif rel_x is not None and rel_x < 0:
            up = -rel_x
        if rel_y is not None and rel_y > 0:
            right = rel_y
        elif rel_y is not None and rel_y < 0:
            left = -rel_y
        rel_move_cursor(up=up, down=down, left=left, right=right)
    rendered: list = nyx_obj.graphic.tolist()
    rendered = ["".join("██" if val == 1 else "  " for val in row) for row in rendered]
    right_offset = f"\033[{right}C" if right > 0 else ""
    rendered = f"\n{right_offset}".join(rendered)
    print(rendered)


def rel_move_cursor(up=0, down=0, right=0, left=0):
    if up > 0:
        sys.stdout.write(f"\033[{up}A")
    if down > 0:
        sys.stdout.write(f"\033[{down}B")
    if right > 0:
        sys.stdout.write(f"\033[{right}C")
    if left > 0:
        sys.stdout.write(f"\033[{left}D")
    sys.stdout.flush()


def abs_move_cursor(row: int = 0, col: int = 0):
    sys.stdout.write(f"\033[{row};{col}H")
    sys.stdout.flush()


graphic = nd.ones((20, 20), dtype="u1")
asset = NyxGraphicAsset(payload=graphic)
print("Raw NyxGraphicAsset")
print(asset.payload)

tilemap = TileMapComponent()
tilemap.graphic = asset.payload
print("\nRendered TileMapComponent:")
render(tilemap)

graphic = nd.array(
    [
        [0, 0, 1, 0, 0],
        [0, 0, 1, 0, 0],
        [1, 1, 1, 1, 1],
        [0, 0, 1, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0],
    ],
    dtype="u1",
)
graphic = 1 - graphic  # invert
asset = NyxGraphicAsset(payload=graphic)
sprite = Sprite()
sprite.graphic = asset.payload
rel_move_cursor(up=10)
print("\033[31m", end="", flush=True)
render(sprite, rel_y=10)
print("\033[0m", end="", flush=True)
