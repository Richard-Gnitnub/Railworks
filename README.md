
# **CAD Pipeline for Railworks Project**

## **Overview**
The **Railworks CAD Pipeline** is a modular framework for generating and exporting **parameterized 3D models** such as **tracks, timbers, tiles, walls, and assemblies**. It integrates:
- **Django** for backend logic
- **Django Ninja** for API management
- **CadQuery** for parametric CAD operations
- **Django Database Cache** for caching API responses and computed models

This project eliminates **static file storage risks** by dynamically generating and securely serving **STEP/STL files** via an API.

---

## **Contributing**

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit changes and push:
   ```bash
   git commit -m "Added new feature"
   git push origin feature-name
   ```
4. Submit a pull request.

---

## **Directory Structure**

```plaintext
dev2/
├── railworks_project/            # Django project configuration
│   ├── __init__.py
│   ├── settings.py               # Configures the project settings
│   ├── urls.py                   # URL routing
│   ├── wsgi.py                   # WSGI entry point
│   ├── asgi.py                   # ASGI entry point
│
├── cad_pipeline/                 # Core app for CAD logic
│   ├── __init__.py
│   ├── models/                   # Centralized models for database
│   │   ├── __init__.py
│   │   ├── assembly.py           # Model for assemblies
│   │   ├── exported_file.py      # Tracks exported files (e.g., STL, STEP)
│   │   ├── nmra_standards.py     # NMRA compliance standards
│   │   ├── parameter.py          # Parameters for CAD generation
│   │   ├── seed_database.py      # Script for seeding the database with initial data
│   ├── cad_engine/               # CAD generation logic
│   │   ├── __init__.py
│   │   ├── assemblies/           # Assemblies for components
│   │   │   ├── __init__.py
│   │   │   ├── tiles/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── tile_generator.py
│   │   │   ├── walls/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── wall_generator.py
│   ├── api/                      # API endpoints
│   │   ├── __init__.py
│   │   ├── assembly_api.py       # API for handling assemblies
│   │   ├── parameter_api.py      # API for handling parameters
│   │   ├── nmra_standard_api.py  # API for NMRA compliance
│   │   ├── schemas/
│   │   │   ├── assembly_schema.py
│   │   │   ├── parameter_schema.py
│   ├── configs/                  # Configuration files
│   │   ├── __init__.py
│   │   ├── config.yaml           # YAML configuration file
│   │   ├── config.py             # Configuration loader
│   ├── helpers/                  # Centralized helpers
│   │   ├── __init__.py
│   │   ├── brick_geometry.py     # Handles 3D brick creation
│   │   ├── cache_manager.py      # Caching utilities
│   │   ├── door_cutout.py        # Boolean cutouts for doors/windows
│   │   ├── export_handler.py     # Unified export logic
│   │   ├── generator.py          # Master function for CAD generation
│
├── tests/                        # Testing framework
│   ├── __init__.py
│   ├── test_models.py            # Tests for models
│   ├── test_api.py               # Tests for API endpoints
│   ├── test_pipeline.py          # Tests for the CAD pipeline
│
├── manage.py                     # Django management script
```

---

## **Database Design**

| **Model**         | **Description** | **Key Fields** |
|------------------|--------------------------------|------------------------------|
| `Assembly` | Stores track, wall, and building assemblies. | `name`, `model_type`, `nmra_standard`, `metadata`, `is_deleted` |
| `ExportedFile` | Tracks exported CAD files. | `assembly`, `file_name`, `file_path`, `file_format`, `generated_at` |
| `NMRAStandard` | Stores NMRA gauge and scale standards. | `name`, `scale_ratio`, `gauge_mm`, `rail_profile` |
| `Parameter` | Stores configurable CAD parameters. | `name`, `value`, `parameter_type` |

---

## **CAD Pipeline Workflow**

```plaintext
+-------------------+
| Input Parameters  |  <-- YAML/JSON (e.g., dimensions, features)
|-------------------|
| - Dimensions      |
| - Roof Details    |
| - Window Specs    |
| - Door Specs      |
+-------------------+
          |
          v
+-------------------+
|  Component Cache  |  <-- Checks if components exist
|-------------------|
| - Brick Tiles     |
| - Windows         |
| - Doors           |
+-------------------+
          |
          v
+---------------------------+
| Intermediate Solid Gen    |  <-- Creates walls, roofs, cutouts
|---------------------------|
| - Generate Walls          |
| - Create Roof             |
| - Add Chimney             |
| - Make Cutouts            |
+---------------------------+
          |
          v
+---------------------------+
|    Dynamic Assembly       |  <-- Combines components
|---------------------------|
| - Align Walls             |
| - Attach Roof             |
| - Position Chimney        |
| - Place Windows/Doors     |
+---------------------------+
          |
          v
+---------------------------+
|  Export and Cache         |  <-- Save STEP/STL files securely
|---------------------------|
| - Secure File Delivery    |
| - Serve API Response      |
+---------------------------+
```

---

## **Django Ninja API**

### **Endpoints**

- **Assemblies**:
  - `GET /api/assemblies/` – Retrieve all assemblies.
  - `GET /api/assembly/{id}/` – Retrieve a single assembly.
- **NMRA Standards**:
  - `GET /api/nmra/{name}/` – Retrieve NMRA standard by name.
- **Parameters**:
  - `GET /api/parameters/{parameter_type}/` – Retrieve all parameters by type.

---

## **How Caching Works**

```plaintext
+-------------------------------+
| User Requests Model via API   |
+-------------------------------+
            |
            v
+-------------------------------+
| Check Database Cache          |
| (Django Database Cache Table) |
+-------------------------------+
    |                |
    | Cache Hit      | Cache Miss
    |                v
    |        +--------------------------+
    |        | Generate CAD Model (API) |
    |        +--------------------------+
    |                      |
    v                      v
+-----------------+     +-----------------------+
| Cache Model URL | <-- | Store in Cache Table |
+-----------------+     +-----------------------+
            |
            v
+---------------------------+
| Serve Secure Model to User |
+---------------------------+
```

---
