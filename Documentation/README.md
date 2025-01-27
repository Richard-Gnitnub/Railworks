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

1. Install dependencies:
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

