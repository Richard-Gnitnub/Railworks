# TODO List

## 1. Project Setup
- [x] Transitioned the framework to Django.  
- [x] Established Django project and core application structure.  
- [x] Installed dependencies for Django, CadQuery, and related tools.  
- [x] Validate new project setup with end-to-end tests (e.g., admin panel accessibility). 
- [x] implemented daisy UI to the admin
- [x] Test on Docker
- [x] Setup Dockercloud
- [x] Setup CI/CD pipeline
- [x] Write contribution guidelines
- [x] Install Ruff linter, setup and auto fix
- [x] Setup Docker Hub
- [x] Setup Docker cloud for builds
- [x] Setup Dependabot
- [x] Install coverage
- [x] Push to github
- [ ] Setup Dev containers to prepare for Cadquery
- [x] Install Cadquery
- [x] Orientate to Cadquery
- [ ] Develop Core functionality Cadquery scripts
- [ ] Run test scripts in staging docker build
- [ ] Merge to main when tests pass

---

## 2. Core Functionality

### a. Database Models
- [x] Migrated models (`Track`, `Gauge`, `Chair`, `Timber`, `STLDownloadLog`) from SQLModel to Django ORM. 
- [x] Update model Chair model naming convention, `BullheadChairs`, `Bullhead BossAndFerrule`, `BullheadKey`, `BullheadJawSection`.
- [x] Test model relationships and ensure data integrity through Django admin and tests.  

### b. Geometry and STL Export
 - [x] Installed CadQuery Editor (CE) and verified it runs in a separate environment.
 - [ ] Develop standalone CadQuery scripts for core STL generation features (e.g., timber and chair integration).
 - [ ] Validate standalone CadQuery scripts using sample data.
 - [ ] Test CadQuery scripts in a staging Docker build to ensure compatibility.
 - [ ] Refine CadQuery scripts based on test results for edge cases and geometry issues.
 - [ ] Prepare scripts for integration with Django views.
 - [ ] Adapt STL generation to integrate with Django views.
 - [ ] Validate STL integrity and provide feedback on issues via Django. 

### c. User Interface
- [ ] Create forms or APIs in Django to allow users to download stls.  
- [ ] Provide functionality for STL file download.  

---

## 3. Testing
- [ ] Add Django-specific unit tests for models and views.  
- [ ] Validate edge cases (e.g., invalid inputs, extreme values for parameters).  
- [ ] Test updated STL generation and export.  

---

## 4. Documentation
- [x] Updated README with new framework and goals.  
- [ ] Create a troubleshooting guide specific to Django.  
- [ ] Add examples for admin panel operations (CRUD for track components).  

---

## 5. Deployment
- [ ] Test the application in a Dockerised environment with Django.  
- [ ] Document deployment steps for Django in Docker.  

---

## 6. Future Enhancements
- [x] Marked FastAPI-specific tasks as deprecated.  
- [ ] Focus on post-MVP enhancements, including turnouts, curves, and advanced STL checks.  
