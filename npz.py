from collections import deque
from datetime import datetime
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
    return input("Enter the folder name: ")


def choose_premade_demo() -> Tuple[str, str, str]:
    """Prompt the user to choose a premade demo.

    Returns:
        Tuple[str, str, str]: The folder, frame prefix, and text for the chosen demo.
    """

    print("Choose a GIF to display:")
    print("1. Doom 2016")
    print("2. Ori and the Blind Forest")
    while True:
        response = input("Select a number")
        if response == "1":
            folder = "doom_2016"
            frame_prefix = "doom"
            text = (
                "Starting Demo:\nDoom 2016\n\nPress the\n\n[ENTER] key\n\nto continue."
            )
            break
        elif response == "2":
            folder = "ori_2"
            frame_prefix = "ori"
            text = "Starting Demo:\nOri and the\nBlind Forest\n\nPress the\n\n[ENTER] key \n\nto continue."
            break
        else:
            print(
                "\033[38;5;2mInvalid selection. Please select a number from the list.\033[0m"
            )

    return folder, frame_prefix, text

def notify_user():
    return "If you can still read this, you need to ZOOM OUT Press [ENTER] to continue."

def trim_odd_frame_row(frame: np.ndarray) -> np.ndarray:
    """Trim the last row of the frame if it is odd.

    Args:
        frame (np.ndarray): The frame to trim.

    Returns:
        np.ndarray: The trimmed frame.
    """
    h = frame.shape[0]
    if h % 2 != 0:
        frame = frame[: h - 1, :]
    return frame


def get_frame_deque(filepath: str) -> Tuple[Deque[np.ndarray], int, int]:
    """Get the frame deque and frame dimensions from an NPZ file.

    Args:
        filepath (str): The filepath to the NPZ file.

    Returns:
        Tuple[Deque[np.ndarray], int, int]: The frame deque, height, and width.

    Raises:
        FileNotFoundError: If the npz demo file is not found.
    """
    frame_imports: Deque[np.ndarray] = deque()
    try:
        npz = NyxAssetImport.open_npz_asset(filepath)
    except FileNotFoundError as err:
        raise err
    for frame_key in npz:
        frame = trim_odd_frame_row(npz[frame_key])
        frame_imports.append(frame)
    return frame_imports, frame.shape[0], frame.shape[1]


def print_grid(h: int, w: int):
    """Print a grid to the terminal to help the user resize the terminal.

    Args:
        h (int): The height of the grid.
        w (int): The width of the grid.
    """
    # Account for subpixel sizing
    h = h // 2

    # Define the corner and border characters
    top_left = "┌"
    top_right = "┐"
    bottom_left = "└"
    bottom_right = "┘"
    cross_border_left = "├"
    cross_border_right = "┤"
    top_cross_border = "┬"
    bottom_cross_border = "┴"
    middle_cross_border = "┼"

    # Relocate the cursor to the top left corner
    print(TerminalUtils.cursor_to_origin())
    # Print the top border
    print(top_left + top_cross_border * (w - 2) + top_right)
    # Print the grid body
    for i in range(h - 2):
        print(cross_border_left + middle_cross_border * (w - 2) + cross_border_right)
    # Print the bottom border
    print(bottom_left + bottom_cross_border * (w - 2) + bottom_right)


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
    print(TerminalUtils.reset_format())


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
    letters = NyxAssetImport.open_npz_asset("block_chars/block_chars")

    try:
        filename = f"{folder}/{frame_prefix}_1"
        npz = NyxAssetImport.open_npz_asset(filename)
    except FileNotFoundError as err:
        raise err
    while True:
        print(TerminalUtils.clear_term())
        print_block_text(
            "Starting the doom\n2016 GIF Demo\n\nPress the\n[ENTER] key.",
            letters,
            hemera_term_api,
        )
        for frame_key in npz:
            frame_imports.append(npz[frame_key])
        if len(frame_imports) > 0:
            print(TerminalUtils.reset_format())
            print_ruler(h, w)
            print(hemera_term_api.ansi_fg[3])
            response = input(
                "If you can still read this, you need to ZOOM OUT!"
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
            if response == "":
                break

    # Clear the terminal before the first run
    TerminalUtils.clear_term()

    fps = 15
    sleep_len = 1 / fps
    start_time = datetime.now()
    while True:
        start_time = datetime.now()
        new_frame = frame_imports.popleft()
        frame_imports.append(new_frame)
        hemera_term_api.print(new_frame)
        time.sleep(sleep_len - (datetime.now() - start_time).seconds)
