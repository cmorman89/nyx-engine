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

NyxEngine is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)**.

### What This Means:
- **You Can:**
  - Use, share, and adapt NyxEngine for **non-commercial purposes**.
  - Modify and share the code, as long as you credit the original author (Charles Morman).

- **You Cannot:**
  - Use NyxEngine for **commercial purposes** without prior written permission.

### Full License:
See the [LICENSE](LICENSE) file or visit [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) for more information.

### Commercial Use
For commercial licensing, please contact nyx-engine@cmorman.com.
