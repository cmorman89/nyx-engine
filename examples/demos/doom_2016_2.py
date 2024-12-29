from collections import deque
from datetime import datetime
import time
from typing import Deque
import numpy as np
from nyx.hemera_term_fx.hemera_term_fx import HemeraTermFx
from nyx.hemera_term_fx.term_utils import TerminalUtils
from nyx.nyx_engine.utils.nyx_asset_import import NyxAssetImport


folder = "planet-earth-sm"
frame_prefix = "planet-earth"


def print_ruler(h: int, w: int):
    line = "+" * w
    for _ in range(h // 2):
        print(line)


if __name__ == "__main__":
    # Clear the terminal before any output
    TerminalUtils.clear_term()

    # Load Early Managers, Stores, Assets, Systems
    hemera_term_api = HemeraTermFx()
    # Load tiles from .nyx files (generate the filename pattern)
    # Save them to a dict (make a deque later)
    frame_imports: Deque[np.ndarray] = deque()
    first_import = True
    h, w = 0, 0
    i = 1
    while True:
        print(hemera_term_api.ansi_fg[3], end ="\r")
        print(TerminalUtils.cursor_abs_move(4, 4), end="\r")
        print(f"Importing frame {i}{"." * ((i//5) % 5)}     ", end="\r")
        try:

            filename = f"{folder}/{frame_prefix}-1-frame{i}"
            tile = NyxAssetImport.open_asset(filename)
            frame_imports.append(tile)
            i += 1
            if first_import:
                temp_frame = frame_imports.pop()
                h, w = temp_frame.shape
                frame_imports.append(temp_frame)
                print(TerminalUtils.cursor_to_origin(), end="\r")
                print(TerminalUtils.reset_format())
                print_ruler(h, w)
                first_import = False

        except FileNotFoundError as err:
            if len(frame_imports) > 0:
                print(TerminalUtils.cursor_to_origin(), end="\r")
                print(TerminalUtils.reset_format())
                print_ruler(h, w)
                print(hemera_term_api.ansi_fg[3])
                input(
                    "All files loaded from disk. Press [ENTER] to start HemeraTermFx."
                    + "\n\n"
                    + "** NOTE: You will need to decrease the terminal font size to a very small "
                    + "size for larger frames. **"
                    + "\n\n"
                    + "The '+' signs form a grid the same size as the render window for this video."
                    + " Resize the terminal or decrease the font size until the '+' form a clear "
                    + "rectangle on the screen."
                    + "\n\n"
                    + "In many terminals, this can be achieved by holding the 'ctrl' key while "
                    + "scrolling the mouse wheel, or holding the 'ctrl' key and pressing the '-' "
                    + " or '+' key. Touchscreens often support pinch-to-zoom in the terminal."
                )
                break
            else:
                raise err

    # Clear the terminal before the first run
    TerminalUtils.clear_term()

    frame_i = 0
    frame_count = len(frame_imports)
    fps = 15
    sleep_len = 1 / fps
    start_time = datetime.now()
    while True:
        start_time = datetime.now()
        new_frame = frame_imports.popleft()
        frame_imports.append(new_frame)
        hemera_term_api.print(new_frame)
        time.sleep(sleep_len - (datetime.now() - start_time).seconds)
