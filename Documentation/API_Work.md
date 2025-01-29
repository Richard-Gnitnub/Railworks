### API Review and Proposed Updates

#### **Current State of API**
- **Base URL**: `/api/v1/`
- **Framework**: Django Ninja
- **Existing Endpoints**:
  - `GET /tiles` — Fetch a list of available tile designs.
  - `POST /tiles/export` — Export a pre-defined tile to supported formats.

#### **Proposed Enhancements**
To align with the new functionality for YAML-configurable Flemish bond tiles, the API documentation requires updates for the following:

---

### **Updated Endpoints**

#### **1. Submit YAML Configuration**
- **Endpoint**: `POST /api/configs/`
- **Description**: Submit a YAML configuration for dynamic tile generation.
- **Request Body**:
  ```json
  {
      "config": "<YAML_CONTENT_AS_STRING>",
      "name": "string (optional, human-readable name)",
      "description": "string (optional, a short description)"
  }
  ```
- **Response**:
  - **200 OK**:
    ```json
    {
        "status": "success",
        "message": "Configuration file validated and stored successfully.",
        "config_id": "string"
    }
    ```
  - **400 Bad Request**:
    ```json
    {
        "status": "error",
        "message": "Invalid configuration file.",
        "errors": ["list of validation errors"]
    }
    ```

#### **2. Trigger Tile Generation**
- **Endpoint**: `POST /api/tiles/generate/`
- **Description**: Generates Flemish bond tiles based on a submitted configuration or inline parameters.
- **Request Body**:
  ```json
  {
      "config_id": "string (optional, references a stored configuration)",
      "parameters": {
          "tile_width": "int (optional, overrides config)",
          "row_repetition": "int (optional, overrides config)",
          "export_formats": ["step", "stl"]
      }
  }
  ```
- **Response**:
  - **200 OK**:
    ```json
    {
        "status": "success",
        "message": "Tile generated and exported successfully.",
        "files": [
            {
                "format": "stl",
                "url": "https://example.com/resources/tiles/v2.0/flemish_tile_v2.0.stl"
            },
            {
                "format": "step",
                "url": "https://example.com/resources/tiles/v2.0/flemish_tile_v2.0.step"
            }
        ]
    }
    ```
  - **400 Bad Request**:
    ```json
    {
        "status": "error",
        "message": "Invalid parameters or configuration.",
        "errors": ["list of validation errors"]
    }
    ```

#### **3. Export Tile**
- **Endpoint**: `GET /tiles/export`
- **Description**: Export the generated tile to the requested file format.
- **Query Parameters**:
  - `tile_id`: ID of the generated tile.
  - `format`: Desired export format (e.g., `stl`, `step`).
- **Response**:
  - **200 OK**:
    Returns the file in the requested format.
  - **400 Bad Request**:
    ```json
    {
        "error": "Invalid format",
        "details": "Unsupported export format: svg"
    }
    ```

#### **4. Fetch Tile Metadata**
- **Endpoint**: `GET /tiles/metadata`
- **Description**: Retrieve metadata for previously submitted configurations or generated tiles.
- **Query Parameters**:
  - `tile_id` (optional): ID of the tile to fetch metadata for.
- **Response**:
  - **200 OK**:
    ```json
    {
        "tile_id": "config_id_1234",
        "submitted_on": "2025-01-28T18:30:00Z",
        "config_details": {
            "tile_width": 5,
            "row_repetition": 3,
            "brick_length": 200,
            "brick_width": 100,
            "brick_height": 50,
            "offset_X": 0,
            "offset_Y": 0
        },
        "generated_files": {
            "step": "/media/resources/tiles/v2.0/flemish_tile_v2.0.step",
            "stl": "/media/resources/tiles/v2.0/flemish_tile_v2.0.stl"
        }
    }
    ```

---

### **Backend Requirements for New Endpoints**

1. **Database Updates**:
   - Add a `TileConfiguration` model to store YAML configuration details and metadata.
   - Add a `GeneratedTile` model to store file paths and tile metadata.

2. **Configuration Validation**:
   - Use `yaml_config.validate_config()` for `POST /tiles/config`.

3. **File Management**:
   - Integrate with the `export_tile` function to save exported files in user-accessible locations.

4. **Asynchronous Tasks**:
   - Implement Celery tasks for tile generation and file export to prevent blocking API requests.

5. **Documentation**:
   - Update OpenAPI schema with new endpoints and expected responses.

---

### **Next Steps**
1. Update the API codebase to include the new endpoints.
2. Modify database models to support configuration storage.
3. Implement Celery for asynchronous tasks.
4. Revise the OpenAPI documentation and test the updated API endpoints thoroughly.

Does this align with the project’s current requirements and future goals? Let me know if changes are needed before proceeding.

