We need to update the **README.md** file to align with the **tile generator workflow** documentation and recent API enhancements. Below is a **comprehensive merge update** of the **README.md** with **no omissions**:

---

# **README: Dynamic Tile Generation System for Railworks Project**

## **Overview**
This project provides a **modular** and **scalable** framework for dynamically generating **3D model tiles** using **CadQuery**, **Django Ninja** for API interactions, and **YAML-based configuration files**. The system is designed to support **multiple tile types**, including:
- **Flemish Brick Bond Tiles**
- **Plain Track Tiles**
- Future expandable **custom tile configurations**

The **API** provides a **RESTful interface** for defining, generating, and exporting tiles in **STEP** and **STL** formats.

---

## **Project Structure**
The **directory structure** is optimized for **scalability**, **separation of concerns**, and **maintainability**.

```
/resources
│
├── /configs                # YAML configuration files for tiles
│   ├── /bricks
│   │   └── flemish_brick.yaml
│   ├── /tracks
│   │   └── plain_track.yaml
│   └── yaml_config.py      # Functions to load and validate YAML files
│
├── /helpers                # Modular helper functions
│   ├── __init__.py
│   ├── brick_geometry.py   # Functions specific to brick geometry
│   ├── track_geometry.py   # Functions specific to track geometry
│   ├── file_helper.py      # File export and path management
│   ├── config_helpers.py   # Dynamic configuration handlers
│   └── tile_assembly.py    # Logic for placing and structuring tiles
│
├── /tiles                  # Tile creation scripts
│   ├── __init__.py
│   ├── generate_tile.py    # Master tile generation script
│
└── /api                    # API integration for tile generation
    ├── __init__.py
    ├── api.py              # API entry point (Django Ninja setup)
    ├── config_router.py    # Routes for managing configurations
    ├── tile_router.py      # Routes for generating tiles
    ├── helpers_api.py      # Routes for helper functions
    └── urls.py             # Root-level API URL definitions
```

---

## **Tile Generation Pipeline**

The **CAD pipeline** is designed to handle **dynamic parameterized inputs**, **reusable components**, and **efficient caching mechanisms** for **3D model generation and export**.

```
+-------------------+
| Input Parameters  |  <-- YAML-based tile configuration
|-------------------|
| - Tile Type       |
| - Dimensions      |
| - Offsets         |
| - Export Formats  |
+-------------------+
          |
          v
+-------------------+
|  Component Cache  |  <-- Checks if components exist before regeneration
|-------------------|
| - Bricks         |
| - Tracks         |
+-------------------+
          |
          v
+---------------------------+
| Geometry Creation         |  <-- Uses helper functions for tile-specific components
|---------------------------|
| - Generate Bricks         |
| - Generate Tracks         |
| - Apply Chamfering        |
+---------------------------+
          |
          v
+---------------------------+
|    Tile Assembly          |  <-- Places components to form complete tiles
|---------------------------|
| - Align Bricks            |
| - Arrange Tracks          |
| - Apply Offsets           |
+---------------------------+
          |
          v
+---------------------------+
|  Export and Cache         |  <-- Saves files in multiple formats
|---------------------------|
| - Export to media/        |
| - Cache Final Models      |
| - Log Metadata            |
+---------------------------+
```

---

## **Django Ninja API**
The project integrates **Django Ninja** for **type-safe**, **high-performance** API development.

### **Endpoints**
#### **Tile Management**
- `GET /api/tiles/`: List all available tile configurations.
- `POST /api/tiles/generate/`: Generate a tile based on YAML configuration.
- `GET /api/tiles/download/{file_id}/`: Download generated tile.

#### **Configuration Management**
- `GET /api/configs/`: Retrieve stored YAML configurations.
- `POST /api/configs/upload/`: Upload a new configuration.

#### **Helpers**
- `GET /api/helpers/formats/`: Retrieve available export formats.
- `GET /api/helpers/tile-types/`: List supported tile types.

---

## **YAML Configuration Schema**
Each YAML file defines tile-specific parameters. Below is the schema for **`flemish_brick.yaml`**:

```yaml
# General Settings
tile_type: bricks             # Tile type identifier
export_formats:               # Export formats (STEP, STL, etc.)
  - step
  - stl

# Brick Dimensions
brick_length: 250             # Length of a brick
brick_width: 120              # Width of a brick
brick_height: 60              # Height of a brick
mortar_chamfer: 5             # Chamfer size for mortar effect

# Tile Configuration
row_repetition: 4             # Number of rows
tile_width: 6                 # Bricks per row

# Placement Offsets
offset_X: 0                   # Horizontal offset (unused for Flemish bond)
offset_Z: 60                  # Vertical stacking offset (brick height)
```

For **`plain_track.yaml`**, the schema differs:

```yaml
# General Settings
tile_type: plain_track
export_formats:
  - step
  - stl

# Track Dimensions
track_length: 500
track_width: 50
track_height: 30
spacing: 10                  # Spacing between adjacent tracks

# Tile Configuration
row_repetition: 3            # Number of rows
tile_width: 4                # Number of tracks per row
```

---

## **Setup Instructions**
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run migrations:
   ```bash
   python manage.py migrate
   ```
3. Start the Django development server:
   ```bash
   python manage.py runserver
   ```

---

## **Future Enhancements**
1. **Live API Configuration Editing**:
   - Implement an interface to edit YAML configurations directly via the API.
2. **Dynamic Tile Previews**:
   - Add WebSocket-based updates for previewing generated tiles.
3. **Custom Tile Generators**:
   - Allow users to define new tile types with modular geometry functions.

---