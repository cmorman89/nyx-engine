# NyxEngine
An experimental, high-performance game engine and rendering pipeline for the terminal. Written in Python with NumPy.

<table border="0">
  <tr>
    <td>
      <img src="https://github.com/user-attachments/assets/e855c330-f7e9-4021-9a5c-5c03b3cbc759" height="300px" alt="NyxEngine Logo">
    </td>
    <td>
      <img src="stars.gif">
    </td>
  </tr>
</table>

---

## Table of Contents:
- [NyxEngine](#nyxengine)
  - [Table of Contents:](#table-of-contents)
  - [Overview:](#overview)
  - [Setup/Run:](#setuprun)
  - [Concept/Demo:](#conceptdemo)
  - [Expected Features:](#expected-features)
  - [Cosmology/Mythology:](#cosmologymythology)
  - [License](#license)
    - [Full License:](#full-license)
  - [Contact](#contact)

---

## Overview:
NyxEngine is a proof-of-concept game engine and rendering pipeline that outputs to a text-based terminal. It aims to push the boundaries of terminal rendering, with no guarantee of success.

---

## Setup/Run:

Get project and set up script
```cli
git clone https://github.com/cmorman89/nyx-engine
cd nyx-engine
sudo chmod u+x run.sh
```

Run the project demo file:
```cli
./run.sh
```

---

## Concept/Demo:
NyxEngine’s rendering capabilities are demonstrated with this example, rendering `spaceship.png` directly to the terminal. This image utilizes:
1. **256-color extended ANSI codes.**
2. **Subpixel rendering** for increased fidelity without additional character usage.

![Rendering of spaceship.png](https://github.com/user-attachments/assets/c6d36b0d-2fbe-4a08-ba9a-6fd98db5e6ce)
Here is another example of a nostalgic side-scrolling space scene. The artifacting is from the GIF
conversion process and isn't present in the terminal. The judder has been amplified by the GIF as
well.
![alt text](image.png)
![alt text](stars.gif)

---

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

---

## Cosmology/Mythology:

- ### Nyx (`NyxEngine`):
  - In the Greek pantheon, Nyx is a primordial goddess who personifies the night, predating even the
    Olympian gods. She is the daughter of Chaos, the first primordial entity, and the mother of
    numerous powerful deities, including Moros (Doom), Aether (Upper Air), and Hemera (Day). Nyx
    commands immense power and influence, earning the respect and fear of even the mighty Olympians,
    who are said to tremble in her presence. Her dominion over the night and all that it encompasses
    makes her one of the most enigmatic and formidable forces in the cosmos. Despite her vast power,
    Nyx's role is often more subtle, as she works behind the scenes to shape the course of events in
    the universe​.

- ### Moros (`MorosEntityManager`):
  - Moros is the son of Nyx (Night), born without a father, and personifies the inexorable force of
    doom. He is the relentless power that drives all beings—mortal and divine alike—toward their
    fated end, embodying the inevitability of death and destiny. It is said that not even the gods,
    including Zeus, could defy the unyielding nature of Moros and the cosmic laws he represents​


- ### Aether (`AetherRenderer`): 
  - Aether is the son of Nyx (Night) and Erebus (Darkness). He personifies the upper air—the pure,
    bright atmosphere breathed by the gods. Aether is also considered the ethereal medium through
    which the divine realm is perceived, representing the luminous, untainted essence that fills the
    heavens.

- ### Hemera (`HemeraTermFx`):
  - In the Greek pantheon, Hemera is the personification of day and light, the daughter of Nyx
    (Night) and Erebus (Darkness). As the embodiment of light, she dispels the shadows of night,
    bringing clarity and illumination to creation and all within it​

---

## License

NyxEngine is licensed under the **MIT License**.

You are free to use, modify, and distribute this software for personal or commercial purposes, provided that you include the original copyright notice and this permission notice in any copies or substantial portions of the software.

### Full License:
See the [LICENSE](LICENSE) file.

---

## Contact
Contact: nyx-engine@cmorman.com.