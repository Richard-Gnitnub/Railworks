Here's the **updated YAML Configuration Documentation** reflecting the **fully dynamic tile system** that supports multiple **bond patterns** via **brick_tile.yaml**.

---

# **YAML Configuration Guide**

## **Introduction**
The **YAML configuration** defines **tile parameters** dynamically for **any brick layout**. With the latest updates, **bond patterns** (e.g., **Flemish, Stretcher, Stack**) are now configurable, eliminating the need for separate YAML files per tile type.

---

## **Configuration File Location**
All **brick-based tiles** use a **single configuration file**, stored in:

```
resources/configs/
├── brick_tile.yaml  # Single configuration for all brick tile types
```

---

## **Brick Tile Configuration (`brick_tile.yaml`)**
This **unified configuration** allows **dynamic placement patterns** for bricks.

```yaml
# Brick Dimensions (in mm)
brick_length: 250
brick_width: 120
brick_height: 60

# Mortar Chamfer (for simulated mortar gaps)
mortar_chamfer: 5  # Chamfer size applied to edges

# Tile Placement
offset_x: 0
offset_y: 0
offset_z: 0

# Tile Structure
row_repetition: 4  # Number of rows per tile
tile_width: 4  # Number of bricks per row

# 👇 NEW CONFIGURATION FOR BOND PATTERN
bond_pattern: flemish  # Options: "flemish", "stretcher", "stack"

# Export Formats
export_formats:
  - step
  - stl
```

---

## **Parameter Descriptions**
| **Parameter**        | **Description** |
|----------------------|----------------|
| `brick_length`      | Length of each brick. |
| `brick_width`       | Width of each brick. |
| `brick_height`      | Height of each brick. |
| `mortar_chamfer`    | Chamfer size applied to edges to simulate mortar. |
| `offset_x`, `offset_y`, `offset_z` | Control the **alignment** of tiles. |
| `row_repetition`    | Number of **rows per tile**. |
| `tile_width`        | Number of **bricks per row**. |
| `bond_pattern`      | Specifies the **brick placement pattern** (`flemish`, `stretcher`, `stack`). |
| `export_formats`    | File formats for **exporting tiles** (`step`, `stl`). |

---

## **Dynamic Configuration Loading**
The **config_helpers.py** module manages:
1. **Loading the YAML file** dynamically.
2. **Validating required parameters** based on **tile structure**.
3. **Applying bond pattern logic dynamically**.

```python
from resources.helpers.config_helpers import load_config, validate_config

# Example Usage:
config = load_config("brick_tile.yaml")
validate_config(config)

# Access dynamic parameters
bond_pattern = config["bond_pattern"]  # e.g., "flemish"
brick_length = config["brick_length"]
```

---

## **Bond Pattern Logic**
### **Supported Patterns**
- **Flemish Bond** → Alternating **full and half bricks** per row.
- **Stretcher Bond** → **Full bricks only**, offset by **half brick** in alternating rows.
- **Stack Bond** → **Bricks stacked vertically** with no offset.

### **Example Logic Implementation**
This logic is implemented in **tile_assembly.py**:
```python
if bond_pattern == "flemish":
    row_x_offset = config["brick_length"] / 2 if row_index % 2 else 0
elif bond_pattern == "stretcher":
    row_x_offset = config["brick_length"] / 2 if row_index % 2 else 0
elif bond_pattern == "stack":
    row_x_offset = 0  # No offset, bricks are stacked directly
```

---

## **Next Steps**
1. **Verify Bond Pattern API Support**:
   - Ensure `/api/tile/generate/` supports **custom bond patterns**.
   - Allow YAML upload via `/api/configs/upload/`.

2. **Test Tile Generation**:
   - Generate **Flemish Bond, Stretcher Bond, and Stack Bond** using the API.
   - Validate tile assembly correctness.

3. **Optimize YAML Config Parsing**:
   - Add **validation checks** for unsupported **bond patterns**.
   - Implement **error handling** for **missing parameters**.

---

**Would you like to start API testing now? 🚀**