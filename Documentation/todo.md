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
- [x] Created the Flemish bond tile generation script (`flemish_brick_tile.py`).  
- [x] Validated the script integration with Django and OCP CAD Viewer.  
- [x] Added Django Ninja for API schema validation and CRUD operations.  
- [x] Installed Memcached for caching.  

---

## **2. Core Functionality**

### **a. CAD Pipeline**
- [x] Designed the CAD pipeline structure and flow based on Fx Bricks' example.  
- [x] Built the first stage of the CAD pipeline (Flemish bond tile generation).  
- [ ] Modify the pipeline to pull component parameters dynamically from the database.  
- [ ] Implement caching for intermediate solids (e.g., chairs, timbers) in the pipeline.  
- [ ] Optimize the pipeline to minimize redundant computations (e.g., bounding box caching).  

### **b. Database Integration**
- [x] Defined and migrated initial database model for `Assembly`.  
- [ ] Extend models to include chairs, timbers, and tracks.  
- [ ] Enable the pipeline to query these models for parameters.  
- [ ] Log pipeline exports (e.g., STEP/STL files) to track performance.  

### **c. Admin Views**
- [ ] Create admin views for managing the `Assembly`, `Chair`, `Timber`, and `Track` models.  

### **d. Geometry and STL Export**
- [x] Created a Flemish bond tile script with STEP/STL export.  
- [x] Integrated export paths using Django's `MEDIA_ROOT`.  
- [ ] Expand pipeline to log metadata for each export (e.g., dimensions, filename).  
- [ ] Validate STL integrity and provide feedback during export.  

---

## **3. Testing**
- [ ] Write basic tests for the database models to ensure they support the CAD pipeline.  
- [ ] Validate edge cases (e.g., missing or invalid parameters).  
- [ ] Test performance of the caching mechanism for intermediate solids.  

---

## **4. Documentation**
- [x] Updated README with new goals, framework, and setup instructions.  
- [x] Added detailed documentation for the Flemish bond tile script.  
- [x] Updated API documentation to include Django Ninja integration.  
- [ ] Document the CAD pipeline's interaction with the database.  
- [ ] Add examples showing how the pipeline queries and generates components.  

---

## **5. Deployment**
- [ ] Install and integrate Celery for task management.  
- [ ] Test the application in a fully Dockerized environment with Celery and Redis.  
- [ ] Document the deployment steps, including environment variables and service orchestration.  

---

## **6. Future Enhancements**
- [x] Removed FastAPI-specific tasks and migrated them to Django Ninja.  
- [ ] Extend the pipeline to support advanced features (e.g., turnouts, curves).  
- [ ] Explore role-based access control (RBAC) for multi-user workflows.  

---

### **Short-Term Priorities**
1. **Database Integration**:
   - Extend models for chairs, timbers, and tracks.
   - Ensure the pipeline queries these models for its inputs.
2. **Pipeline Optimization**:
   - Add caching for reusable components and subassemblies.
   - Log and store intermediate solid metadata in the database.
3. **Admin Views**:
   - Create and refine admin views for all models.
4. **Task Management**:
   - Install and configure Celery for task queue management.
   - Validate Celery integration with Redis and Docker.
5. **Testing and Validation**:
   - Validate functionality with database-driven inputs.
   - Ensure caching improves performance without breaking outputs.
