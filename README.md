# **CAD Pipeline for Railworks Project**

## **Overview**
The **Railworks CAD Pipeline** is a modular framework for generating and exporting **parameterized 3D models** such as **tracks, timbers, tiles, walls, and assemblies**. It integrates:
- **Django** for backend logic.
- **Django Ninja** for API management.
- **CadQuery** for parametric CAD operations.
- **Django MPTT** for hierarchical database structures.
- **Django Database Cache** for caching API responses and computed models.

This project eliminates **static file storage risks** by dynamically generating and securely serving **STEP/STL files** via an API.

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
│   ├── admin/                    # Django admin configuration
│   ├── api/                      # API endpoints
│   │   ├── __init__.py
│   │   ├── assembly_api.py       # API for handling assemblies
│   │   ├── nmra_standard_api.py  # API for NMRA compliance
│   │   ├── schemas/
│   │   │   ├── assembly_schema.py
│   ├── cad_engine/               # CAD generation logic
│   │   ├── __init__.py
│   │   ├── configs/              # Configuration management
│   │   │   ├── config.yaml       # YAML configuration file
│   │   │   ├── config.py         # Configuration loader
│   │   ├── helpers/              # Specialized helpers for CAD operations
│   │   │   ├── assemble_brick_tile.py
│   │   │   ├── brick_geometry.py
│   │   │   ├── door_cutout.py
│   │   │   ├── fence_helper.py
│   │   │   ├── track_helper.py
│   │   │   ├── wall_helper.py
│   │   ├── export_handler.py     # Unified export logic
│   │   ├── generate_component.py # Generalized component generator
│   ├── management/               # Custom Django management commands
│   ├── migrations/               # Django migrations for database
│   ├── models/                   # Centralized models for database
│   │   ├── __init__.py
│   │   ├── assembly.py           # Model for assemblies (MPTT-based)
│   │   ├── exported_file.py      # Tracks exported files
│   │   ├── nmra_standards.py     # NMRA compliance standards
│   ├── templates/                # HTML templates for Django admin
│   ├── tests/                    # Testing framework
│   │   ├── __init__.py
│   │   ├── test_models.py        # Tests for models
│   │   ├── test_api.py           # Tests for API endpoints
│   │   ├── test_pipeline.py      # Tests for the CAD pipeline
│
├── manage.py                     # Django management script
```

---

## **Database Design**

| **Model**         | **Description**               | **Key Fields**                             |
|--------------------|-------------------------------|--------------------------------------------|
| `Assembly`         | Stores assemblies (e.g., walls, tracks) with hierarchical relationships using MPTT. | `name`, `type`, `parameters`, `parent`    |
| `ExportedFile`     | Tracks exported files.        | `assembly`, `file_name`, `file_format`    |
| `NMRAStandard`     | Stores NMRA compliance data.  | `name`, `scale_ratio`, `gauge_mm`         |

---

## **CAD Engine Overview**

The **`cad_engine/`** module serves as the backbone of the Railworks CAD pipeline, managing **agnostic processes** for CAD operations. These processes are independent of specific assemblies or components, ensuring flexibility and reusability across various workflows. This modular design allows for seamless scaling and efficient processing.

### **Core Agnostic Processes**

1. **`export_handler.py`**:
   - Manages all logic for exporting models into formats like `STEP` and `STL`.
   - Ensures compatibility with caching for optimized exports.

2. **`generate_component.py`**:
   - Orchestrates component generation using input configurations.
   - Delegates specific tasks to helpers like `brick_geometry.py`.

3. **`helpers/`**:
   - Contains specialized helper scripts for various CAD operations, including:
     - `assemble_brick_tile.py`: Handles assembly of brick tiles.
     - `brick_geometry.py`: Handles geometry creation for bricks.
     - `door_cutout.py`: Handles cutouts for doors.
     - `fence_helper.py`: Provides utilities for fences.
     - `track_helper.py`: Provides utilities for track assembly.
     - `wall_helper.py`: Handles wall-related CAD logic.

---

## **Caching Workflow**

```plaintext
+---------------------------+     +------------------------+     +---------------------------+
|        User Input         | --> |   generate_component   | --> |   Django Database Cache    |
| (e.g., Brick Tile Config) |     | (Orchestrates Helpers) |     | (Caches Exported Models)  |
+---------------------------+     +------------------------+     +---------------------------+
                                      |
                                      v
                            +------------------------+
                            |     export_handler     |
                            | (Handles File Exports) |
                            +------------------------+
                                      |
                                      v
                        +--------------------------------+
                        |    Returns Exported Files     |
                        | (STEP/STL Cached or On-Demand)|
                        +--------------------------------+
```

---

## **Django Ninja API**

### **Endpoints**

- **Assemblies**:
  - `GET /api/assemblies/` – Retrieve all assemblies.
  - `GET /api/assembly/{id}/` – Retrieve a single assembly.
- **NMRA Standards**:
  - `GET /api/nmra/{name}/` – Retrieve NMRA standard by name.

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

## **Future Roadmap**
1. Expand NMRA compliance handling with additional rail profiles.
2. Add new helpers for complex assemblies like buildings with nested components.
3. Optimize caching for faster pipeline execution.
4. Introduce additional export formats, such as `3MF` and `OBJ`.
5. Enhance API endpoints with authentication and user-specific caching.

---

Let me know if any further updates or refinements are needed!