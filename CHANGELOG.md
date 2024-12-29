# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com), 
and this project adheres to [Semantic Versioning](https://semver.org).

---

## [UNRELEASED]
### Added
- Import npz files for multiple frames or sprites.

### Changed
- Refactor `HemeraTermFx` to further optimize terminal printing performance.

---

## [0.1.0-alpha] - 2024-12-27
### Added
- New method and hooks in `HemeraTermFx` to enable line profiling for performance testing.
- GIF demos in the `examples\demos` folder to showcase the project's capabilities.
- Add an alient planet sprite to the current game demo in `main.py`.

### Changed
- Optimize terminal printing string generation for a 95% reduction in frame printing time.

---

## [0.0.4-alpha] - 2024-12-22
### Added
- Add unit testing for `NyxEntity`, `ComponentManager` and `MoraiEntityManager`
- Add documentation for `NyxEntity`, `ComponentManager`, and `MoraiEntityManager`
- Implemented printing/rendering moving sprites to the terminal.
- Implemented `NyxEngine` for orchestrating the central game loop and managing resources.
- Tilemap rendering now supports infinite scrolling in all directions.
  
### Changed
- Switch `entity_id` to an integer instead of `UUID` for easier readability and indexing in `NyxEntity`.
- Simplify `MoraiEntityManager` by removing friendly name lookup/mapping and providing a method to clear the registry.
- Simplify `ComponentManager` with less nested logic and simpler output. Components organized by type for fast system access.
- Tilemap printing now uses a dedicated helper/manager `TilemapManager` and is no longer a `NyxSystem`.
- Significant README and project documentation updates -- including animated demos of current project state.
- Begin refactoring `demo.py` to use the new `NyxEngine` and allow for better usability and clarity.

### Fixed
- Incorrect printing iteration caused excessive new lines in animated sprites.

### Regression
- Terminal size updates are no longer working correctly. Manual window sizes must be specified.
  
### Removed
  - Removed `NyxComponentStore`, `TilesetStore`, `TilemapSystem` as they are directly replaced by `ComponentManager` and `TilemapManager`.

---

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
  - Implemented an animated, nostalgic starfield tilemap using the new rendering pipeline.

### Changed
- Renamed `HemeraRenderer` to `HemeraTermFx` as it handles terminal effects and rendering.
- Renamed `AetherCompositor` to `AetherRenderer` as it manages the rendering pipeline.
- Renamed `NyxEntityManager` to `MoraiEntityManager` to reflect the project's mythology/consistency.

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