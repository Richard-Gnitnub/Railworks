# Flemish Bond Brick Pattern – Implementation Documentation

## Overview
The Flemish Bond pattern consists of alternating full and half bricks per row.

- **Odd rows (0, 2, 4…)** start with a half brick, followed by a full brick.
- **Even rows (1, 3, 5…)** start with a full brick, followed by a half brick.
- Each even row is offset by half a brick to align half-brick centers with full brick centers.

## Flemish Bond Algorithm

### Step 1: Create a New Row Assembly
Each row is created as a CadQuery assembly:

```python
row_assembly = cq.Assembly()
```

Each row has an X-offset (`x_offset`) that determines brick placement.

- Even rows get a negative shift (`-brick_length / 2`) so they align properly.

### Step 2: Place Bricks in the Row
Loop through each column (`tile_width`) and alternate full and half bricks.
The first row starts with a half brick, while the next row starts with a full brick.

#### Even Rows (Shifted)

```python
if i % 2 != 0:  # If row index is even
    row_x_offset = -config["brick_length"] / 1.5  # Shift row left by half a brick
```

#### Brick Placement Logic

```python
if j % 2 == 0:  # Every even index gets a full brick
    row_assembly.add(full_brick, loc=cq.Location(cq.Vector(x_offset, 0, 0)))
    x_offset += config["brick_length"]
else:  # Every odd index gets a half brick
    row_assembly.add(half_brick, loc=cq.Location(cq.Vector(x_offset, 0, 0)))
    x_offset += config["brick_length"] / 2
```

This ensures:
✅ Full bricks and half bricks are flush together.
✅ Even rows shift correctly, aligning half-brick centers with full brick centers below.

### Step 3: Apply Vertical Stacking
After placing bricks in the row, we stack rows on top of each other:

```python
z_offset = i * config["brick_height"]
tile_assembly.add(row_assembly, loc=cq.Location(cq.Vector(offset_X * i, 0, z_offset)))
```

This stacks the next row above the previous row.

## How to Extend This for Other Bond Patterns
The same row-based approach can be applied to other wall types:

### 1️⃣ Stretcher Bond
🔹 Rows of full bricks, staggered by half a brick per row.

Every row gets the same shift:

```python
row_x_offset = -config["brick_length"] / 2
```

Brick placement remains the same.

### 2️⃣ Stack Bond
🔹 Bricks are placed directly on top of each other (no staggering).

Remove all offsets:

```python
row_x_offset = 0
```

Every row looks identical.

### 3️⃣ English Bond
🔹 Alternates between rows of full bricks and rows of half bricks.

- **Odd rows**: Full bricks only.
- **Even rows**: Half bricks only.

```python
if i % 2 == 0:  # Odd rows
    place_full_bricks()
else:  # Even rows
    place_half_bricks()
```

