# **TODO List**

## **1. Project Setup**
- [x] Transitioned the framework to Django.  
- [x] Established Django project and core application structure.  
- [x] Installed dependencies for Django, CadQuery, and related tools.  
- [x] Validated new project setup with end-to-end tests (e.g., admin panel accessibility).  
- [x] Installed and configured DockerCloud for builds.  
- [x] Setup CI/CD pipeline.  
- [x] Wrote contribution guidelines.  
- [x] Installed Ruff linter and applied fixes.  
- [x] Setup Dependabot for dependency management.  
- [x] Installed coverage and integrated it into CI pipelines.  
- [x] Pushed the project to GitHub.  
- [x] Installed and tested CadQuery.  
- [x] Created the Flemish bond tile generation script (`assemble_brick_tile.py`).  
- [x] Validated the script integration with Django and OCP CAD Viewer.  
- [x] Added Django Ninja for API schema validation and CRUD operations.  
- [x] Configured Django MPTT for hierarchical database relationships.  
- [x] Replaced `parameter.py` with dynamic JSON fields in the database.  
- [x] Removed `cache_manager.py` and integrated caching directly into export workflows.  
- [x] Installed Django Database Cache for efficient caching.  

---

## **2. Core Functionality**

### **a. CAD Pipeline**
- [x] Designed the CAD pipeline structure and flow based on Fx Bricks' example.  
- [x] Built the first stage of the CAD pipeline (`assemble_brick_tile.py`).  
- [x] Centralized logic using a dynamic `generate_component.py` for unified CAD generation.  
- [ ] Modify the pipeline to pull component parameters dynamically from the database.  
- [ ] Implement caching for intermediate solids (e.g., chairs, timbers) in the pipeline.  
- [ ] Optimize the pipeline to minimize redundant computations (e.g., bounding box caching).  
- [x] Integrated STEP and STL export functionalities via `export_handler.py`.  
- [ ] Implement error handling and validation for STL/STEP exports.  

### **b. Database Integration**
- [x] Defined and migrated initial database model for `Assembly` using Django MPTT.  
- [x] Integrated hierarchical relationships for parent-child assemblies (e.g., walls, tiles, tracks).  
- [x] Added the `ExportedFile` model to track exported files.  
- [x] Replaced individual parameters with dynamic JSON-based `parameters` in the `Assembly` model.  
- [x] Extended database to support NMRA standards (`nmra_standards.py`).  
- [ ] Extend models to include reusable components like chairs, timbers, and tracks.  
- [ ] Enable the pipeline to query these models dynamically for parameter inputs.  
- [ ] Log detailed metadata for each pipeline export (e.g., dimensions, file size, format).  

### **c. Admin Views**
- [x] Created admin views for managing `Assembly` and `ExportedFile` models.  
- [ ] Add admin views for managing NMRA standards and new component models.  
- [ ] Improve UI/UX for admin panel interactions, including inline editing.  

### **d. Geometry and STL Export**
- [x] Created the Flemish bond tile generation script with STEP/STL export.  
- [x] Integrated export paths using Django's `MEDIA_ROOT`.  
- [x] Enabled caching of STEP/STL exports to avoid redundant computation.  
- [ ] Log export metadata (e.g., dimensions, file format, size) to the database.  
- [ ] Validate STL and STEP integrity during the export process.  

---

## **3. Testing**
- [ ] Write comprehensive unit tests for all database models, including MPTT relationships.  
- [ ] Validate edge cases (e.g., missing or invalid parameters, circular dependencies).  
- [ ] Test performance of caching mechanisms for intermediate solids and assemblies.  
- [ ] Write integration tests for API endpoints (e.g., assembly creation, export workflows).  
- [ ] Conduct load testing to evaluate system scalability.  

---

## **4. Documentation**
- [x] Updated README with project goals, framework, and updated setup instructions.  
- [x] Added detailed documentation for the `assemble_brick_tile.py` script.  
- [x] Updated API documentation to reflect Django Ninja integration.  
- [x] Documented the use of MPTT for hierarchical assemblies.  
- [ ] Add examples showcasing how the pipeline queries the database and generates components.  
- [ ] Document caching strategies for reusable components and exports.  

---

## **5. Deployment**
- [ ] Install and integrate Celery for task management.  
- [ ] Test the application in a fully Dockerized environment with Celery and Redis.  
- [ ] Document deployment steps, including environment variables, Docker orchestration, and Celery setup.  
- [x] Added Docker configurations (`Dockerfile` and `docker-compose.yaml`).  
- [ ] Optimize deployment for production environments (e.g., load balancing, security).  

---

## **6. Future Enhancements**
- [x] Removed FastAPI-specific tasks and migrated to Django Ninja.  
- [ ] Extend the pipeline to support advanced features (e.g., turnouts, curves, multi-layer assemblies).  
- [ ] Explore role-based access control (RBAC) for multi-user workflows.  
- [ ] Introduce a visualization dashboard for assembly relationships using D3.js or similar.  
- [ ] Implement robust error tracking and notifications (e.g., Sentry integration).  
- [ ] Investigate front-end integration for parameter adjustments and live previews.  

---

## **MVP Roadmap**

### **MVP1: Core Pipeline & Basic Functionality**
✅ Basic parametric model for brick tiles (Flemish bond).  
✅ Integrated database-driven parameter storage.  
✅ Established Django framework, admin panel, and API structure.  
✅ Implemented STEP and STL export functionality.  

### **MVP2: Brick/Tiling Expansion**
- Additional bond patterns (Stretcher, English, Herringbone).  
- Improved boundary handling (half-bricks, offsets, corners).  
- Enhanced parametric control (mortar thickness, brick dimensions).  
- Integration of cutouts (doors, windows).  
- Improve caching strategy to store computed patterns for reuse.  

### **MVP3: Advanced Geometry & UX Improvements**
- Multi-layered/complex brick structures.  
- Improved validation and logging for exports.  
- Admin interface enhancements for parameter tuning.  
- API refinements for more dynamic parameter handling.  

### **MVP4: Async Tasks, Scalability, and Collaboration**
- Celery/RQ integration for handling long-running CAD operations.  
- Role-based access control for different user permissions.  
- Optimisation for caching and performance at scale.  
- Implement asynchronous processing of export tasks.  

### **MVP5: Advanced Features & Visualisation**
- Interactive 3D preview of brick patterns.  
- Full-fledged parameter library for users to select presets.  
- Expansion into additional architectural components and assemblies.  
- Support for exporting additional file formats (e.g., OBJ, 3MF).  

---

## **Short-Term Priorities**
1. **Database Integration**:
   - Extend models for chairs, timbers, and tracks.
   - Ensure the pipeline dynamically queries these models for its inputs.
2. **Pipeline Optimization**:
   - Add caching for reusable components and subassemblies.
   - Log and store detailed metadata for intermediate and final exports.
3. **Admin Views**:
   - Refine admin views to include all new models and hierarchical relationships.
4. **Task Management**:
   - Install and configure Celery for task queue management.
   - Validate Celery integration with Redis and Docker.
5. **Testing and Validation**:
   - Ensure caching improves performance without affecting functionality.
   - Validate assembly generation workflows with real-world scenarios.  

