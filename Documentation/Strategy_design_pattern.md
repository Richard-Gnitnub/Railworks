```plaintext
          +----------------------------------+
          |         AbstractGenerator        |  <-- (Context)
          |----------------------------------|
          | - generator_strategy: IGenerator |
          | - generate_object(assembly): ... |
          +---------------+------------------+
                          |
                          | (calls `generate()`)
                          v
               +----------------------+          +-----------------------+
               |      IGenerator     |  <-- (Strategy Interface)       |
               |----------------------|          |-----------------------|
               | + generate(assembly)|          | + generate(assembly)  |
               +----------+----------+          +-----------+-----------+
                          |                               |
                          | (implements)                  | (implements)
                          v                               v
        +---------------------------+          +----------------------------+
        | ConcreteWallGenerator    |          | ConcreteBrickTileGenerator|
        |---------------------------|          |----------------------------|
        | + generate(assembly): ...|          | + generate(assembly): ...  |
        +---------------------------+          +----------------------------+
```
---
Here is your content in Markdown format:

```markdown
# Strategy Pattern for Assembly Generation

## Step-by-Step Implementation

### 1. Create a Strategy Interface (`IGenerator`)

- Define a method `generate(assembly: Assembly) -> cq.Workplane`.
- This method signature will be the same across all concrete generators, ensuring consistency.

### 2. Implement Concrete Strategies

- **`ConcreteWallGenerator`** implements `IGenerator` and handles all logic for generating a wall (calculating dimensions, applying cutouts, exporting files, etc.).
- **`ConcreteBrickTileGenerator`** implements `IGenerator` and contains tile-specific logic (arranging bricks, exporting files, etc.).
- Additional types (e.g. “building” or “roof”) can be implemented as separate concrete strategies.

### 3. Abstract Generator as the Context

- The `AbstractGenerator` (or a similarly named class) holds a reference to an `IGenerator` (e.g., `generator_strategy`).
- When the user triggers generation (through the UI or another input), `AbstractGenerator` retrieves the `assembly` from the database, determines its type, and assigns the appropriate concrete strategy.

#### Example:

```python
if assembly.type == "wall":
    self.generator_strategy = ConcreteWallGenerator()
elif assembly.type == "brick_tile":
    self.generator_strategy = ConcreteBrickTileGenerator()
# Additional cases as needed...
```

- `AbstractGenerator` then calls `self.generator_strategy.generate(assembly)`, delegating the actual build/export logic to the appropriate concrete strategy.

### 4. Avoid Filename Verbosity

- Each concrete generator should handle its own naming logic, using user-defined parameters for the export filename.
- This prevents excessive name concatenation across parent-child relationships.

### 5. UI Integration

- The UI allows users to define or override parameters, including custom naming conventions.
- When the user clicks **"Generate"**, the system calls `AbstractGenerator.generate_object(assembly)`, which:
  1. Sets the correct `IGenerator` strategy.
  2. Executes the generation logic.
- If recursion is required (e.g., generating child assemblies first), `AbstractGenerator` can handle it by retrieving children from the database and generating them sequentially or bottom-up.

---

## Benefits of This Approach

- **Flexibility**: Easily add new generator types (e.g., a “foundation” or “roof” generator) without modifying the existing code.
- **Maintainability**: Common logic (like retrieving assemblies or storing exports) resides in `AbstractGenerator`, while each generator strategy handles only the specifics of its assembly type.
- **Scalability**: By cleanly separating concerns, the codebase remains organised and avoids duplication as it grows.
```

This format makes the content structured, easy to read, and suitable for documentation. Let me know if you need any modifications! 🚀

