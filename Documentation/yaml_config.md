# **Documentation Update**

## **1. YAML Integration**

### Overview
The script `flemish_brick_tile.py` now supports YAML configurations for defining key parameters dynamically, improving flexibility and maintainability.

### Configuration Directory
- YAML configuration files are stored in the `resources/configs/` directory.
- The default configuration file is `default_config.yaml`.

### Example YAML Configuration
```yaml
# Default configuration for brick and mortar dimensions
brick_length: 200
brick_width: 100
brick_height: 50
mortar_length: 300
mortar_width: 90
mortar_height: 10
```

### Usage
The script loads configurations dynamically using:
```python
from resources.tiles.flemish_brick_tile import load_config
config = load_config()
```

### Validation
- The `validate_config` function ensures all required keys are present.
- Raises `ValueError` if keys are missing.

## **2. Testing Framework**

### Overview
Tests are located in `resources/tests/test_flemish_brick_tile.py` and validate:
- YAML configuration integration.
- Geometry generation for full bricks, half bricks, and mortar rows.
- Export functionality, including error handling.

### Key Tests

#### YAML Tests
- `test_load_config`: Ensures valid YAML configurations load correctly.
- `test_validate_config`: Verifies proper validation for complete configurations.
- `test_validate_config_missing_key`: Confirms that missing keys raise appropriate errors.

#### Geometry Tests
- `test_create_full_brick_aligned`: Uses parameterized tests to validate brick dimensions.
- `test_create_half_brick_aligned`: Ensures correct dimensions for half bricks.
- `test_create_mortar_row_layer`: Verifies mortar dimensions dynamically.

#### Export Tests
- `test_export_tile_with_yaml_config`: Ensures STEP and STL files export correctly using YAML-defined dimensions.
- `test_invalid_export_directory`: Validates handling of non-existent directories.
- `test_empty_tile_export`: Confirms the script raises errors for empty tiles.

### Command to Run Tests
```bash
pytest resources/tests/test_flemish_brick_tile.py -v
```

## **3. Export Functionality**

### Supported File Types
- **STEP** (.step): High-fidelity CAD format.
- **STL** (.stl): Standard for 3D printing.

### Example Output Directory
Exports are saved under `media/resources/tiles/` in versioned subdirectories:
```
media/
├── resources/
│   ├── tiles/
│   │   ├── v1.0/
│   │   │   ├── flemish_tile_v1.0.step
│   │   │   ├── flemish_tile_v1.0.stl
```

### Export Function
Exports are handled by the `export_tile` function:
```python
def export_tile(tile, version="v1.0"):
    output_dir = os.path.join(settings.MEDIA_ROOT, "resources", "tiles", f"v{version}")
    os.makedirs(output_dir, exist_ok=True)
    exporters.export(tile.toCompound(), os.path.join(output_dir, f"flemish_tile_{version}.step"))
    exporters.export(tile.toCompound(), os.path.join(output_dir, f"flemish_tile_{version}.stl"))
```

## **4. Example YAML Configurations**

### Default Configuration
```yaml
brick_length: 200
brick_width: 100
brick_height: 50
mortar_length: 300
mortar_width: 90
mortar_height: 10
```

### Test Configuration
```yaml
brick_length: 250
brick_width: 120
brick_height: 60
mortar_length: 350
mortar_width: 100
mortar_height: 15
```

### Custom Configuration
For larger bricks and thinner mortar:
```yaml
brick_length: 300
brick_width: 150
brick_height: 75
mortar_length: 320
mortar_width: 80
mortar_height: 8
```