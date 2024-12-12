# NyxEngine
An experimental, high-performance game engine and rendering pipeline for the terminal. Written in Python with NumPy.

<img src="https://github.com/user-attachments/assets/e855c330-f7e9-4021-9a5c-5c03b3cbc759" height="300px" alt="NyxEngine Logo">

## Overview:
NyxEngine is a proof-of-concept game engine and rendering pipeline that outputs to a text-based terminal. It aims to push the boundaries of terminal rendering, with no guarantee of success.

## Expected Features:
- **Rendering:**
  - Standard and 256-color extended ANSI support.
  - Delta-only rendering to optimize performance by updating only changed pixels.
  - Runbuffer detection for contiguous blocks of ANSI codes.
  - Subpixel rendering: Simulates higher resolution using foreground/background colors and special characters (e.g., ▀, ▄).

- **Data:**
  - Save and load assets to JSON for easy sharing.
  - Save and load assets to PNG for external tools.
  - Group, layer, and compose NumPy matrices for sprites, animations, and scenes.

- **Engine:**
  - Side-scrolling games.
  - Room-based map exploration.
  - Open-world environments.
  - Full keyboard support for input handling.

- Plus more to come as the project evolves!

## Concept/Demo:
NyxEngine’s rendering capabilities are demonstrated with this example, rendering `spaceship.png` directly to the terminal. This image utilizes:
1. **256-color extended ANSI codes.**
2. **Subpixel rendering** for increased fidelity without additional character usage.

![Rendering of spaceship.png](https://github.com/user-attachments/assets/c6d36b0d-2fbe-4a08-ba9a-6fd98db5e6ce)

## License

NyxEngine is licensed under the **MIT License**.

You are free to use, modify, and distribute this software for personal or commercial purposes, provided that you include the original copyright notice and this permission notice in any copies or substantial portions of the software.

### Full License:
See the [LICENSE](LICENSE) file.

### Contact
Contact: nyx-engine@cmorman.com.
