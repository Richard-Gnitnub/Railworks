# **README: CAD Pipeline for Railworks Project**

## **Overview**
This project provides a modular framework for designing and exporting parameterized 3D models, including reusable components like tracks, timbers, chairs, and buildings (e.g., lineside huts). It leverages Django for the backend, Django Ninja for API management, and CadQuery for CAD operations.

---

## **Directory Structure**
The project directory structure is organized for scalability and clarity:

```plaintext
dev2/
├── railworks_project/            # Django project configuration
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── apps/
│   ├── cad/                      # CAD-related operations (e.g., geometry generation)
│   │   ├── __init__.py
│   │   ├── pipelines/
│   │   │   ├── flemish_bond.py
│   │   │   ├── solid_cache.py
│   │   │   ├── line_side_hut.py
│   │   ├── exporters/
│   │   │   ├── step_exporter.py
│   │   │   ├── stl_exporter.py
│   ├── resources/                # Stores reusable models (chairs, timbers)
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── api.py
│   │   ├── serializers.py
│   ├── tracks/                   # Handles track-specific components
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── api.py
│   │   ├── serializers.py
├── media/                        # Stores generated files (STEP/STL)
│   ├── resources/
│   │   ├── tiles/
│   │   │   ├── v1.0/
│   │   │   │   ├── flemish_tile_v1.0.step
│   │   │   │   ├── flemish_tile_v1.0.stl
├── manage.py                     # Django management script




/cad_pipeline
│
├── /cad_engine              # Core CAD logic
│   ├── generator.py         # Master function for CAD model generation
│   ├── model_loader.py      # Loads models from DB
│   ├── export_handler.py    # Unified export logic (STEP/STL/GLTF)
│   ├── cache_manager.py     # Caches reusable components
│   ├── /tiles               # TILE GENERATION MODULE
│   │   ├── tile_generator.py   # Unified tile creation logic
│   │   ├── flemish_brick.py   # Specific pattern logic
│   │   ├── stretcher_bond.py   # Other patterns
│
├── /models                  # Modular CAD components
│   ├── /assemblies          # Organized by category
│   │   ├── /walls           # Wall-related assemblies
│   │   │   ├── wall_generator.py   # Full wall generation logic
│   │   │   ├── cutouts.py          # Handles openings (doors/windows)
│   │   ├── /track           # Track-related assemblies
│   │   │   ├── bullhead_track.py
│   │   │   ├── turnout.py
│   │   ├── /buildings       # Buildings & structures
│   │   │   ├── signal_box.py
│   │   │   ├── platform_shelter.py
│   │   │   ├── station_building.py
│
├── /cad_engine/helpers       # Centralized helpers
│   ├── brick_geometry.py    # Handles 3D brick creation
│   ├── brick_placement.py   # Handles brick placement (Flemish, Stretcher, etc.)
│   ├── door_cutout.py       # Handles Boolean cutouts for doors/windows
│   ├── caching.py           # Cache utilities for models
│
├── /database                # Database models & migrations
│
├── /api                     # API for requesting CAD models
│
└── /tests                   # Unit tests





```

---

## **CAD Pipeline Logic**

The **CAD pipeline** is designed to handle dynamic parameterized inputs, reusable components, and efficient caching mechanisms for 3D model generation and export.

```plaintext
+-------------------+
| Input Parameters  |  <-- YAML/JSON (e.g., building dimensions, features)
|-------------------|
| - Dimensions      |
| - Roof Details    |
| - Window Specs    |
| - Door Specs      |
+-------------------+
          |
          v
+-------------------+
|  Component Cache  |  <-- Check if components already exist
|-------------------|
| - Brick Tiles     |
| - Windows         |
| - Doors           |
+-------------------+
          |
          v
+---------------------------+
| Intermediate Solid Gen    |  <-- Create walls, roofs, cutouts
|---------------------------|
| - Generate Walls          |
| - Create Roof             |
| - Add Chimney             |
| - Make Cutouts            |
+---------------------------+
          |
          v
+---------------------------+
|    Dynamic Assembly       |  <-- Assemble components into the full model
|---------------------------|
| - Align Walls             |
| - Attach Roof             |
| - Position Chimney        |
| - Place Windows/Doors     |
+---------------------------+
          |
          v
+---------------------------+
|  Fillet and Decorate      |  <-- Finalize edges, engrave details
|---------------------------|
| - Smooth Edges            |
| - Add Text Engravings     |
| - Apply Aesthetic Details |
+---------------------------+
          |
          v
+---------------------------+
|  Export and Cache         |  <-- Save STEP/STL files for reuse
|---------------------------|
| - Export to media/        |
| - Cache Final Models      |
| - Log Metadata            |
+---------------------------+
```
---
## Caching Strategy

```
+-------------------------------+
| User Requests Tile Generation |
+-------------------------------+
            |
            v
+-------------------------------+
| Generate Cache Key (Hash)     |
+-------------------------------+
            |
        (Check Cache)
        /         \
      Yes         No
     /             \
Retrieve        Generate CAD Model
From Cache      (Only if Necessary)
     \             /
      \           /
  +-----------------------+
  | Serve Model to User   |
  +-----------------------+

```
## Cache Plan

```

+------------------------------+
| User Requests Model via API  |
+------------------------------+
            |
            v
+-------------------------------+
| Check Memcached for Model     |  <-- 🔹 If cached, return instantly
+-------------------------------+
    |                |
    | Cache Hit      | Cache Miss
    |                v
    |        +--------------------------+
    |        | Generate CAD Model (API) |
    |        +--------------------------+
    |                      |
    v                      v
+-----------------+     +---------------------------------+
| Cache Model URL | <-- | Upload to Secure Storage (S3) |
+-----------------+     +---------------------------------+
            |
            v
+---------------------------+
| Serve Secure Signed URL   |  <-- 🔹 File expires after short period
+---------------------------+

Final Security and Performance Strategy
Component	Technology	Purpose
Fast CAD model retrieval	Memcached	Reduces unnecessary recomputation
Secure file storage	AWS S3 / MinIO (private bucket)	Prevents direct file exposure
Access control	JWT authentication	Ensures only authorized users request models
Cache expiry handling	Memcached TTL & manual invalidation	Prevents stale results
Scalability	Docker + Kubernetes (future-ready)	Allows handling large-scale requests

```

---

## **Key Features**

1. **Dynamic Input Parsing**:
   - Supports YAML/JSON configurations for defining component dimensions and customization options.
2. **Caching**:
   - Efficiently stores and reuses intermediate solids to reduce computation time.
3. **Dynamic Assembly**:
   - Combines individual components (e.g., walls, roofs) into a complete model.
4. **Export**:
   - Outputs STEP/STL files to `media/` for reuse or 3D printing.

---

## **Django Ninja API**

The project integrates **Django Ninja** for fast, type-safe API development. Key endpoints include:

- **Components**:
  - `GET /api/components/`: Retrieve available components (e.g., chairs, timbers).
  - `POST /api/components/`: Add a new component configuration.
- **STL Generation**:
  - `POST /api/stl/generate/`: Generate STL based on parameters.
  - `GET /api/stl/status/<task_id>/`: Check generation task status.
  - `GET /api/stl/download/<file_id>/`: Download the generated STL.

---

## **Setup**

1. Clone this repository

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run migrations:
   ```bash
   python manage.py migrate
   ```
3. Start the development server:
   ```bash
   python manage.py runserver
   ```

