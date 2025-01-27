# Flemish Bond Tile Script Documentation

## Overview
This script, `flemish_brick_tile.py`, generates a Flemish bond tile using perfectly aligned bricks and mortar layers. The tile is visualized using the OCP CAD Viewer in VS Code, and it exports watertight STEP and STL files for use in 3D modeling or printing.

## Project Context
This script is part of the `railworks_project` and resides in the `resources/tiles/` directory. The exported files are saved in the global `media/` folder under `resources/tiles` in versioned subfolders.

## Script Breakdown

### File Location
```
dev2/
├── railworks_project/
│   ├── settings.py
│   ├── ...
├── resources/
│   ├── tiles/
│   │   ├── flemish_brick_tile.py
├── media/
│   ├── resources/
│   │   ├── tiles/
│   │   │   ├── v1.0/
│   │   │   │   ├── flemish_tile_v1.0.step
│   │   │   │   ├── flemish_tile_v1.0.stl
```

### Key Features
- **Django Integration:** Leverages Django’s settings for path handling and export directories.
- **OCP CAD Viewer:** Renders the tile during development.
- **Parameterized Design:** Allows easy customization of brick and mortar dimensions.
- **File Export:** STEP and STL files are exported to versioned directories.

## Django Integration
The script integrates with Django by:

- Adding the project root to `sys.path` for module discovery.
- Configuring the `DJANGO_SETTINGS_MODULE` to point to `railworks_project.settings`.
- Using `settings.MEDIA_ROOT` to define export paths.

## How to Run the Script

### Prerequisites
- **Virtual Environment:** Ensure the `.venv` virtual environment is activated.

  ```bash
  .venv\Scripts\activate
  ```

- **Dependencies:**
  - CadQuery
  - OCP CAD Viewer
  - Django

- **Project Setup:**
  - Ensure the `DJANGO_SETTINGS_MODULE` is correctly set in `settings.py`.
  - Verify `MEDIA_ROOT` is defined in the settings:

    ```python
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
    ```

### Execution
Run the script from the project root:

```bash
python resources/tiles/flemish_brick_tile.py
```

## Expected Output

### OCP CAD Viewer:
- The Flemish bond tile should render in the viewer.

### Exported Files:
- Files are saved in the global media folder:

  ```bash
  media/resources/tiles/v1.0/flemish_tile_v1.0.step
  media/resources/tiles/v1.0/flemish_tile_v1.0.stl
  ```

## Key Functions

### Brick and Mortar Creation
- `create_full_brick_aligned()`: Creates a full brick.
- `create_half_brick_aligned()`: Creates a half brick.
- `create_mortar_row_layer()`: Creates a mortar layer.

### Row Creation
- `create_first_row()`: Creates the first row of bricks.
- `create_second_row()`: Creates the second row (mortar layer).
- `create_third_row()`: Creates the third row of bricks.

### Tile Assembly
- `create_flemish_tile()`: Combines rows into a complete tile assembly.

### File Export
- `export_tile(tile, version="v1.0")`: Exports the tile to STEP and STL formats in versioned subdirectories under `MEDIA_ROOT`.

## Troubleshooting

### Common Errors
- **`ModuleNotFoundError: No module named 'railworks_project'`**
  - Ensure the `sys.path.append()` line correctly points to the project root.
  - Verify the project structure matches the expected layout.

- **`ImproperlyConfigured: Requested setting MEDIA_ROOT, but settings are not configured.`**
  - Confirm `DJANGO_SETTINGS_MODULE` is set and `settings.py` includes `MEDIA_ROOT`.

- **Missing Export Files**
  - Check for permission issues or invalid paths in the `settings.MEDIA_ROOT`.

### Debugging
- Use the debug statement to verify the Python path:

  ```python
  print("Python Path:", sys.path)
  ```

