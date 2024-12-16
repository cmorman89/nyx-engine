# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com), 
and this project adheres to [Semantic Versioning](https://semver.org).

## [UNRELEASED]
### Added
- Add unit testing for `NyxEntity`, `ComponentManager` and `MoraiEntityManager`
- Add documentation for `NyxEntity`, `ComponentManager`, and `MoraiEntityManager`
  
### Changed
- Switch `entity_id` to an integer instead of `UUID` for easier readability and indexing in `NyxEntity`.
- Simplify `MoraiEntityManager` by removing friendly name lookup/mapping and providing a method to clear the registry.
- Simplify `ComponentManager` with less nested logic and simpler output. Components organized by type for fast system access.


## [0.0.3-alpha] - 2024-12-13
### Added
- **Delta Framebuffer Rendering**:
  - Implemented delta-based framebuffer to track and render only changed pixels.
  - Utilized stacked NumPy matrices to track foreground (fg) and background (bg) colors separately.
  - Printing optimized with sparse updates by skipping unchanged pixels.
- **Subpixel Rendering**:
  - Enabled subpixel resolution using doubled height rendering.
  - Updated calculations to support 256-color tilemaps rendered with subpixels.
- **File Imports**:
  - Introduced `.nyx` file import system for loading assets as arrays, converted to ndarrays.
- **Refactoring and Documentation**:
  - Added docstrings across all modules for improved maintainability.
  - Refactored `AetherRenderer` into a main class and supporting utility classes.
  - Updated file structure and naming conventions for clarity.
- **Readme Enhancements**:
  - Introduced mythology section to explain the naming scheme.
  - Added static and animated screenshots/screen captures, exemplifying the terminal output when rendering.
- **Demo**:
  - Provided basic "run.sh" bash script to use to launch the demo.
  - Implemented an animated, nostalgic starfield tilemap using the new rendering pipeline.

### Fixed
- Debugged 3D-to-2D matrix iteration issues causing misaligned axes and anomalous subpixel rendering patterns.
- Resolved cursor relocation inaccuracies during delta rendering, improving visual fidelity and performance.

---

## [0.0.2-alpha] - 2024-12-08
### Added
- **Tilemap Rendering**:
  - Rendered tilemaps to the terminal using subpixel resolution.
  - Integrated foreground (fg) and background (bg) colors for zero tiles and gaps.
- **Caching and Storage**:
  - Tilemaps are buffered after computation to improve performance.
  - Implemented a `TilesetStore` class for managing and storing tilemaps by ID.
- **Position and Scene Components**:
  - Introduced `PositionComponent` for potential scrolling functionality.
  - Added `SceneComponent` as a global container/flag for managing tilemaps.

---

## [0.0.1-alpha] - 2024-12-07
### Added
- **Background Rendering**:
  - Rendered solid color backgrounds to the terminal using 256-color ANSI codes.
  - Allowed resizing of background rendering smaller than the terminal dimensions.
- **Core ECS Framework**:
  - Established core ECS with abstract base classes (`NyxEntity`, `NyxSystem`, `NyxComponent`) for modular development.
  - Built foundational rendering systems: `NyxComponentStore`, `RendererSystem`, `AetherCompositor`, and `HemeraRenderer`.
- **Basic Terminal Utilities**:
  - Created `term_utils.py` for common terminal operations.

---

### Notes
- **Milestones Achieved**:
  - [0.0.1-alpha]: First functional pipeline (ECS → Render → Output).
  - [0.0.2-alpha]: Added Tilemap rendering and subpixel support.
  - [0.0.3-alpha]: Introduced delta framebuffer rendering and comprehensive documentation.
- Development methodology favored building systems layer by layer, starting from the background layer and moving upward through the rendering pipeline.
