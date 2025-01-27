# **CAD Pipeline Documentation**

## **Purpose**
The CAD pipeline is the backbone of the Railworks Project, enabling dynamic and efficient generation of 3D models based on parameterized inputs. This document outlines the design, flow, and logic of the pipeline, ensuring clarity for development, debugging, and future enhancements.

---

## **Pipeline Overview**
The pipeline processes user-defined inputs to produce detailed 3D models. It optimizes performance using caching, modular components, and a structured flow from input parsing to final export.

### **Pipeline Stages**

1. **Input Parameters**
   - Accepts YAML or JSON files specifying the model’s dimensions, features, and customizations.
   - Example:
     ```yaml
     building:
       dimensions:
         width: 100
         depth: 80
         height: 60
       roof:
         pitch: 30
         overhang: 5
       windows:
         count: 2
         dimensions: [10, 15]
         positions:
           - left
           - right
       door:
         width: 15
         height: 25
         position: center
     ```

2. **Component Caching**
   - Checks if reusable components (e.g., brick tiles, windows, doors) already exist.
   - Avoids redundant computations by loading pre-cached components.

3. **Intermediate Solid Generation**
   - Creates structural elements such as walls, roofs, and cutouts for doors/windows.
   - Subdivided into modular functions for each component.

4. **Dynamic Assembly**
   - Combines individual components into a unified model.
   - Applies transformations (positioning, rotation) based on input parameters.

5. **Fillet and Decorate**
   - Adds finishing touches, such as fillets for smooth edges and engraved text.

6. **Export and Cache**
   - Saves final STEP and STL files in structured directories.
   - Logs metadata for traceability and potential reuse.

---

## **Detailed Workflow**

### **1. Input Parameters**
#### **Role**:
Defines the high-level model specifications, such as dimensions, materials, and features.

#### **Output**:
A parsed data structure that feeds subsequent stages.

### **2. Component Caching**
#### **Role**:
Minimizes computation by reusing previously generated components.

#### **Flow**:
1. **Check Cache**: Query the cache using a unique identifier (e.g., hash of parameters).
2. **Load Component**: If available, load the cached STEP file.
3. **Generate and Save**: If not cached, create the component and store it.

### **3. Intermediate Solid Generation**
#### **Role**:
Generates modular components (walls, roofs, doors) based on input specifications.

#### **Flow**:
1. Generate a base shape using extrusion or other operations.
2. Apply transformations (e.g., cutting for openings).
3. Save the resulting solid for use in assembly.

### **4. Dynamic Assembly**
#### **Role**:
Combines generated components into a complete model.

#### **Flow**:
1. Load components (cached or freshly generated).
2. Align and position components relative to each other.
3. Merge into a unified assembly.

### **5. Fillet and Decorate**
#### **Role**:
Enhances realism and aesthetics.

#### **Flow**:
1. Apply fillets to predefined edges.
2. Add text engravings or other decorative details.

### **6. Export and Cache**
#### **Role**:
Saves the final model and logs metadata for reuse and auditing.

#### **Flow**:
1. Save the model as STEP and STL files.
2. Store metadata, such as dimensions and export timestamps.
3. Cache the final model for potential reuse.

---

## **Caching Strategy**

### **Component Cache**
- Stores intermediate solids (e.g., walls, roofs) to avoid redundant generation.
- Uses a hashed identifier based on parameters for lookup.

### **Final Model Cache**
- Saves fully assembled models to reduce regeneration time for identical configurations.
- Versioning ensures traceability and avoids overwriting.

---

## **Performance Considerations**
1. **Optimized Caching**:
   - Reduces computation time by reusing components and models.
2. **Parallel Processing**:
   - Utilize Celery workers for asynchronous generation tasks.
3. **Scalable Design**:
   - Modular pipeline stages allow easy integration of new components.

---

## **Examples**

### **Lineside Hut Workflow**
1. **Input**:
   - YAML specifies hut dimensions, roof pitch, and features.
2. **Component Loading**:
   - Load cached brick tiles, windows, and doors.
3. **Solid Generation**:
   - Create walls, roof, and cutouts for openings.
4. **Assembly**:
   - Align walls, roof, and chimney.
5. **Export**:
   - Save as STEP and STL files in versioned directories.

---

## **Future Enhancements**
1. **Advanced Features**:
   - Support for turnouts, curved tracks, and other complex components.
2. **Dynamic Textures**:
   - Apply surface textures for enhanced realism.
3. **Enhanced Scalability**:
   - Add support for distributed processing to handle larger models.

---

This document serves as the reference for implementing, debugging, and extending the CAD pipeline. Let me know if you’d like to refine specific sections or add more details! 🚀

