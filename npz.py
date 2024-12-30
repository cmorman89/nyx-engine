from collections import deque
from datetime import datetime
from operator import le
from random import randint
import time
from typing import Deque
import numpy as np
from nyx.hemera_term_fx.hemera_term_fx import HemeraTermFx
from nyx.hemera_term_fx.term_utils import TerminalUtils
from nyx.nyx_engine.utils.nyx_asset_import import NyxAssetImport


# TODO:
# ---
# Prompt user:
# Prompt user for folder
# Prompt user for frame prefix
# Prompt user for original FPS
# Notify user of terminal font size requirements
# Notify user of terminal resizing requirements
# Print ruler to help user resize terminal
# Prompt user to press enter to start
# ---
# Cleanup:
# Remove unnecessary loops
# ---
# Functions:
# Trim uneven frame height
# Limit view to ONLY the render window (build a camera)
# ---


folder = "doom_2016"
frame_prefix = "doom"


def get_folder():
    pass


def get_frame_prefix():
    pass


def get_fps():
    pass


def notify_user():
    pass


def trim_odd_frame_row(frame: np.ndarray, h: int, w: int):
    if frame.shape[0] % h != 0:
        frame = frame[: h - 1, :]
    return frame


def print_ruler(h: int, w: int):
    line = "+" * w
    for _ in range(h // 2):
        print(line)


def print_block_text(
    text: str, letters, hemera_term_api: HemeraTermFx, color: int = randint(0, 255)
):
    text = text.lower()
    color = min(max(color, 0), 255)
    letter_h, letter_w = letters["a"].shape
    letter_gap = np.zeros((6, 1))
    lines = text.split("\n")
    w = max([len(line) for line in lines]) * (letter_w + letter_gap.shape[1])
    line_gap = np.zeros((2, w))
    block_matrix = None
    block_line = None
    for i, line in enumerate(lines):
        block_line = np.zeros((letter_h, 0))
        for j, letter in enumerate(line):
            block_line = np.hstack((block_line, letter_gap, letters[letter]))
        # Extend the block_line to the width of the longest line
        block_line = np.hstack(
            (block_line, np.zeros((letter_h, w - block_line.shape[1])))
        )
        if i == 0:
            block_matrix = block_line
        else:
            block_matrix = np.vstack((block_matrix, line_gap, block_line))

    hemera_term_api.print(block_matrix)


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
    letters = NyxAssetImport.open_npz_asset("alpha/alpha")
    print_block_text("Starting the doom\n2016 GIF Demo\n\nPress the ENTER key.", letters, hemera_term_api)
    input(
        "If you can still read this, you need to ZOOM OUT\n Press [ENTER] to continue."
    )

    while True:
        print(hemera_term_api.ansi_fg[3], end="\r")
        print(TerminalUtils.cursor_abs_move(4, 4), end="\r")
        print(f"Importing frame {i}{"." * ((i//5) % 5)}     ", end="\r")
        try:
            filename = f"{folder}/{frame_prefix}_1"
            npz = NyxAssetImport.open_npz_asset(filename)
            for frame_key in npz:
                frame_imports.append(npz[frame_key])

            i += 1
            if first_import:
                temp_frame = frame_imports.pop()
                h, w = temp_frame.shape
                frame_imports.append(temp_frame)
                print(TerminalUtils.cursor_to_origin(), end="\r")
                print(TerminalUtils.reset_format())
                print_ruler(h, w)
                first_import = False
                break

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
