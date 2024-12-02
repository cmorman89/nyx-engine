# NyxEngine
An experimental, high-performance game engine and rendering pipeline for the terminal. Written in Python with NumPy.

## Overview:
NyxEngine is a proof-of-concept attempt at implementing a game engine and rendering pipeline that outputs to a text-based terminal. 

## Expected Features:
- Rendering:
  - Standard and 256-color extended ANSI support.
  - Delta-only rendering to optimize performance.
  - Runbuffer detection for contiguous blocks of ANSI codes.
  - Subpixel rendering for increased fidelity without increasing character count.
- Data:
  - Save and load assets to JSON.
  - Save and load assets to PNG.
  - Group, layer, and compose NumPy matricies.
- Engine:
  - Side-scrolling game
  - Map of rooms game
  - Open world game
  - Full keyboard support
- Plus more to come!

# Concept/Demo:
Rendering of `spacecship.png` to the terminal, utlizing subpixel rendering.
![image](https://github.com/user-attachments/assets/c6d36b0d-2fbe-4a08-ba9a-6fd98db5e6ce)


## License

NyxEngine is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)**.

### What This Means:
- **You Can:**
  - Use, share, and adapt NyxEngine for **non-commercial purposes**.
  - Modify and share the code, as long as you credit the original author ([Your Name Here]).

- **You Cannot:**
  - Use NyxEngine for **commercial purposes** without prior written permission.

### Full License:
See the [LICENSE](LICENSE) file or visit [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) for more information.

### Commercial Use
For commercial licensing, please contact [Your Email/Website].
