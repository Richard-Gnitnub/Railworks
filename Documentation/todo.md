# **TODO List**

## **1. Project Setup**
- [x] Transitioned the framework to Django.  
- [x] Established Django project and core application structure.  
- [x] Installed dependencies for Django, CadQuery, Django Ninja, and related tools.  
- [x] Configured Django Ninja for **schema-based API management**.  
- [x] Created a **Dockerized development environment**.  
- [x] Installed and tested CadQuery.  
- [x] Integrated OCP CAD Viewer for model visualization.  
- [x] Refactored the repository to **separate concerns**, ensuring scalability.  
- [x] Implemented hot reload support for Django.  
- [x] Added **logging and error handling** for STL and STEP exports.  

---

## **2. Core Functionality**

### **a. CAD Pipeline**
- [x] Designed the **CAD pipeline structure** based on modular helpers.  
- [x] Built the first **dynamic tile generation pipeline**.  
- [x] Fully **modularized tile generation** to support multiple patterns.  
- [x] Implemented **brick placement logic** supporting Flemish bond pattern.  
- [x] Made the pipeline **YAML-configurable**, eliminating hardcoded values.  
- [x] Refactored **brick generation into helper functions**.  
- [x] Implemented **dynamic row repetition** and configurable offsets.  
- [x] Added support for **bond pattern selection** (e.g., Flemish, stretcher).  
- [x] Ensured tile export functionality works with **multiple formats**.  
- [ ] Extend support for **additional tile patterns** (e.g., running bond).  
- [ ] Optimize placement logic to **support irregular patterns**.  
- [ ] Implement **tile caching** to avoid redundant computations.  

### **b. Database Integration**
- [ ] Define and migrate **database models** for:
  - Tile types (bricks, track, future additions).
  - Component storage (chairs, timbers, sleepers).
  - STL/STEP **export logs**.
- [ ] Enable the CAD pipeline to **query the database** for parameters dynamically.  
- [ ] Implement **admin controls** to manage tile configurations via Django Admin.  
- [ ] Store **export metadata** (e.g., dimensions, file paths) for tracking.  

### **c. Geometry and STL Export**
- [x] Created a **unified STL/STEP export function** in file helpers.  
- [x] Integrated **Django’s MEDIA_ROOT** for file storage.  
- [x] Added **logging for exports** to track success and failures.  
- [ ] Validate **exported STL/STEP files** for potential errors.  
- [ ] Optimize STL export for **reduced file size and improved mesh quality**.  

---

## **3. API Development**

### **a. Core API Enhancements**
- [x] Implemented Django Ninja for **fast, schema-based API endpoints**.  
- [x] Created **tile generator API** for triggering tile creation.  
- [x] Created API endpoints for **tile configuration retrieval**.  
- [x] Implemented **file download API** for retrieving exported STL/STEP files.  
- [ ] Add **query parameters** to adjust tile generation dynamically.  
- [ ] Implement API endpoint for **uploading custom YAML configurations**.  

### **b. API Testing & Documentation**
- [x] Integrated **Django Ninja’s Swagger UI** for API documentation.  
- [x] Updated API docs to reflect **new dynamic tile functionality**.  
- [x] Added example requests for **tile generation and file downloads**.  
- [ ] Ensure all API endpoints return **consistent, structured responses**.  
- [ ] Implement **unit tests for API endpoints** using pytest.  

---

## **4. Testing & Validation**
- [x] Wrote **unit tests for tile generation functions**.  
- [x] Validated YAML parsing logic with **various configurations**.  
- [x] Ensured **correct placement logic** for Flemish bond pattern.  
- [ ] Test **STL/STEP integrity** before export.  
- [ ] Validate **performance impact** of large tile generations.  

---

## **5. Documentation**
- [x] Updated README with **new framework details** and workflow explanations.  
- [x] Added **detailed YAML configuration documentation**.  
- [x] Documented the **tile generator workflow** for better maintainability.  
- [x] Updated API documentation to reflect **new endpoints and improvements**.  
- [ ] Add a **FAQ section** for common errors and troubleshooting.  

---

## **6. Deployment & CI/CD**
- [ ] Test the application in a fully **Dockerized production environment**.  
- [ ] Integrate **Celery + Redis** for background task processing.  
- [ ] Automate file exports to a **centralized file storage** for retrieval.  
- [ ] Document **deployment steps and best practices**.  

---

## **7. Future Enhancements**
- [ ] Extend the pipeline to **support non-brick tiles** (e.g., plain tracks).  
- [ ] Explore implementing **role-based access control (RBAC)**.  
- [ ] Add **real-time progress updates** for tile generation.  
- [ ] Optimize large-scale STL/STEP **generation for efficiency**.  

---

### **Immediate Priorities**
1. **Database Integration**
   - Implement models for storing tile configurations and STL/STEP logs.
   - Enable querying the database for dynamic tile generation parameters.
2. **Pipeline Optimization**
   - Introduce caching for intermediate solids.
   - Improve performance by reducing redundant tile generation steps.
3. **API Enhancements**
   - Implement query parameters for dynamic tile adjustments.
   - Allow **custom YAML uploads** for flexible tile generation.
