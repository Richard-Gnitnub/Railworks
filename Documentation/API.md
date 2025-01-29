### **Updated API Documentation for Dynamic Tile Generation System**

This update **fully aligns** with the **refactored directory structure, helper functions, and YAML-based tile configurations**. 

---

# **API Design Document for Dynamic Tile Generation**

## **Introduction**
This API provides **a flexible and scalable system** for generating 3D model tiles dynamically. Using **Django Ninja**, the API allows users to:
- **Configure tile parameters using YAML files.**
- **Generate 3D models of different tile types (e.g., bricks, tracks).**
- **Export tiles in multiple formats (STEP, STL).**
- **Retrieve and modify YAML configurations.**

The system is modular and supports adding **new tile types** without significant refactoring.

---

## **API Overview**
- **Framework:** Django Ninja (Fast, schema-based API framework).
- **Authentication:** JWT-based authentication for secure interactions.
- **File Management:** Supports STEP/STL file generation and caching.
- **Scalability:** Uses helper functions for modular and extendable logic.

---

## **1. Tile Generation Endpoints**
These endpoints handle **tile creation, export, and retrieval**.

### **1.1 Generate Tile**
- **`POST /api/tiles/generate/`**
- **Description:** Generates a tile using a YAML configuration file.
- **Request Body (JSON):**
  ```json
  {
    "tile_type": "bricks",
    "config_file": "flemish_brick.yaml"
  }
  ```
- **Response (JSON):**
  ```json
  {
    "message": "Tile generation started",
    "task_id": "12345abcde"
  }
  ```
- **Notes:** 
  - Supports `bricks`, `plain_track`, and other **registered tile types**.
  - Configuration files must be **uploaded** before generating.

---

### **1.2 Download Tile**
- **`GET /api/tiles/download/{file_id}/`**
- **Description:** Retrieve an exported tile (STEP or STL).
- **Response:** Returns the file as an attachment.

---

### **1.3 List Available Tiles**
- **`GET /api/tiles/`**
- **Description:** Returns a list of previously generated tiles.
- **Response (JSON):**
  ```json
  [
    {
      "file_id": "xyz123",
      "tile_type": "bricks",
      "file_path": "/media/resources/tiles/v2.0/flemish_brick.step"
    }
  ]
  ```

---

## **2. Configuration Management**
These endpoints **manage and modify YAML tile configurations**.

### **2.1 List Available Configurations**
- **`GET /api/configs/`**
- **Description:** Lists all stored YAML configurations.
- **Response (JSON):**
  ```json
  [
    "flemish_brick.yaml",
    "plain_track.yaml"
  ]
  ```

---

### **2.2 Retrieve a Specific Configuration**
- **`GET /api/configs/{config_name}/`**
- **Description:** Fetches the content of a given YAML file.
- **Response (YAML as JSON):**
  ```json
  {
    "tile_type": "bricks",
    "brick_length": 250,
    "brick_width": 120
  }
  ```

---

### **2.3 Upload New Configuration**
- **`POST /api/configs/upload/`**
- **Description:** Allows users to upload a new YAML tile configuration.
- **Request Body (YAML File)**
  ```yaml
  tile_type: bricks
  brick_length: 250
  brick_width: 120
  ```
- **Response (JSON):**
  ```json
  {
    "message": "Configuration uploaded successfully",
    "config_name": "custom_brick.yaml"
  }
  ```

---

### **2.4 Modify Existing Configuration**
- **`PUT /api/configs/{config_name}/`**
- **Description:** Updates values in an existing YAML file.
- **Request Body (JSON):**
  ```json
  {
    "brick_length": 300
  }
  ```
- **Response:**
  ```json
  {
    "message": "Configuration updated successfully"
  }
  ```

---

## **3. Helper Endpoints**
These endpoints return **metadata** about the system.

### **3.1 List Supported Tile Types**
- **`GET /api/helpers/tile-types/`**
- **Description:** Returns a list of tile types that can be generated.
- **Response (JSON):**
  ```json
  ["bricks", "plain_track"]
  ```

---

### **3.2 Get Available Export Formats**
- **`GET /api/helpers/formats/`**
- **Description:** Lists supported export formats.
- **Response (JSON):**
  ```json
  ["step", "stl"]
  ```

---

## **4. API Request-Response Flow**
Below is a **visual workflow** of how **API requests are processed**.

```plaintext
+----------------------+       +----------------------+       +----------------------+
|  User Sends Request  | ----> |  Validate YAML File  | ----> |  Generate Tile Model  |
|  (Generate Tile)     |       |  (Check Format, Keys)|       |  (CadQuery Assembly)  |
+----------------------+       +----------------------+       +----------------------+
            |                                      |
            v                                      v
+----------------------+       +----------------------+
|  Store File in /media/ | --> |  Return File Path  |
+----------------------+       +----------------------+
```

---

## **5. Authentication & Security**
- **JWT Authentication**: Used for secure API access.
- **Rate Limiting**: Prevents abuse of high-load endpoints.
- **Validation**: Ensures all YAML configurations conform to expected schemas.

---

## **6. Future Enhancements**
- **WebSocket Integration**: Real-time updates on tile generation progress.
- **Front-End UI**: Web-based YAML editor for modifying configurations.
- **Expanded Tile Library**: More patterns and track configurations.
