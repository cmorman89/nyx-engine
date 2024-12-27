import time
from typing import Dict
import numpy as np
from nyx.aether_renderer.aether_renderer import AetherRenderer
from nyx.hemera_term_fx.hemera_term_fx import HemeraTermFx
from nyx.hemera_term_fx.term_utils import TerminalUtils
from nyx.nyx_engine.utils.nyx_asset_import import NyxAssetImport



if __name__ == "__main__":
    # Load Early Managers, Stores, Assets, Systems
    aether_renderer = AetherRenderer()
    hemera_term_api = HemeraTermFx()

    # Load tiles from .nyx files (generate the filename pattern)
    frame_count = 19
    frames = [f"sb/sb-1-frame{i}" for i in range(1, frame_count)]
    # Save them to a temporary dictionary
    frame_imports: Dict[int, np.ndarray] = {}
    for i, filename in enumerate(frames):
        print(
            f"Importing frame {i + 1}/{frame_count}{"." * ((i//5) % 5)}     ", end="\r"
        )
        tile = NyxAssetImport.open_asset(filename)
        frame_imports[i] = tile

    # Clear the terminal before the first run
    TerminalUtils.clear_term()

    frame_i = 0
    frame_count = len(frames)
    aether_renderer.dimensions.window_h = 144
    aether_renderer.dimensions.window_w = 200
    while True:
        new_frame = frame_imports[frame_i]
        frame_i += 1
        if frame_i >= frame_count or frame_i <= frame_count:
            frame_i = frame_i % frame_count
        hemera_term_api.print(new_frame)

        # time.sleep(2)
        # time.sleep(0.5)
        # time.sleep(1 / 10)  # 10 fps
        # time.sleep(0.0666)  # 15 fps
        # time.sleep(0.0333)  # 30 fps
        time.sleep(0.0222)  #45 fps
        # time.sleep(0.0167)  # 60 fps
        # time.sleep(0.00833)  # 120 FPS
