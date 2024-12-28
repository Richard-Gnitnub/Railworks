# **PROJECT**:  
**Lightweight Track Builder (Rewrite of Templot by Martin Wynne)**  

---

## **GOAL**  
Develop a lightweight Django-based application to design accurate model railway track for 3D printing, focusing on **COT (Chairs on Timbers) track**. This MVP prioritises straight track generation adhering to bullhead rail standards based on REA specifications. The generated STL files include timbers with integrated chairs, and the rail will be manually added post-printing. The MVP serves as a foundation for a modular and extensible track design tool.

## **Test First Approach**
The app will be developed using a test first approach at every stage of development. 

---

## **KEY INSIGHTS**  
- Legacy `dxf_unit.pas` and related Pascal files contain pivotal 2D DXF and 3D STL export logic.  
- Decades of incremental updates have resulted in tightly coupled 2D and 3D geometry.  
- Key insights from COT track analysis:  
  - **COT track**: Single printable unit.  
  - **Chair Data**
  - **Timber Data**
  - **Alignment Patterns** 

---

## **MVP PLAN**  

### **Framework**  
- Build the MVP using **Django** for its robust ORM, admin interface, and scalability.  

### **Core Features**  
- **STL Generation**:  
  - Parameterised straight plain track geometry using REA Bullhead.  
  - COT Track, solid chairs with loose jaws for the crossing rails.
- **Database Integration**:  
  - Models for dynamic track configurations stored in SQLite.  
- **Admin Panel**:  
  - Manage CRUD operations for timbers, chairs, gauges, and track settings. styled with daisy UI. 

### **Excluded from MVP**  
- **Curved Tracks** and **Turnouts** (planned for future enhancements).  
- **Plug track** Highly detailed chairs suitable for resin printing
- **Mesh Inspection and Repair** (post-MVP).
- **UI/UX**
Daisy UI, Tailwind, HTMX.

---
## **PROJECT DIRECTORY STRUCTURE**

```
railworks_project/
    manage.py               # Django management script
    railworks_project/      # Global project configuration
        __init__.py
        settings.py         # Project-level settings
        urls.py             # URL routing
        asgi.py             # ASGI configuration
        wsgi.py             # WSGI configuration
    trackbuilder_app/       # Core application for track design
        __init__.py
        admin.py            # Admin panel configuration
        apps.py             # App-specific settings
        models.py           # Database models for track components
        views.py            # Application views
        urls.py             # App-level URL routing
        tests/              # Unit tests for the application
            __init__.py
            factories.py    # Factory Boy definitions for test data
            test_models.py  # Model tests
        migrations/         # Database migration files
        templates/          # HTML templates for the app
        static/             # Static assets (CSS, JS, images)
    db.sqlite3              # SQLite database file (development only)
    requirements.txt        # List of Python dependencies
    venv/                   # Virtual environment folder
```
---
## **CORE APPLICATION FUNCTIONALITY**  
```
flowchart TD
    A[User Input] -->|Track Parameters| B[Input Validation]
    B -->|Check for Errors| C{Valid Input?}
    C -->|Yes| D[Fetch Data from Database]
    C -->|No| E[Return Error Message]
    D -->|Configurations Loaded| F[Process Geometry]
    F -->|Generate Timbers and Chairs| G[Create 3D Model with CadQuery]
    G -->|Convert to STL| H[STL Export]
    H -->|Save File| I[Provide Download Link]
    I -->|User Access| J[Download STL File]

    subgraph Django Workflow
        B --> C --> D --> F
    end

    subgraph External Logic
        G --> H
    end

    subgraph Final Output
        I --> J
    end
```
---
## **WORKING ENVIRONMENT REQUIREMENTS**

- **Development Tools**:
  - Python 3.8+ (ensure compatibility with the Django version used).
  - Django 4.x for the backend.
  - Docker to avoid it works on my machine and oh, must be your code.
  - Factory Boy for test data generation.

- **Development Environment**:
  - IDE: Visual Studio Code.
  - CLI: Command Prompt (Windows).
  - Version Control: GitHub Desktop.

- **Database**:
  - SQLite

## **SETUP INSTRUCTIONS**

## Clone the Repository**
git clone <repository-url>
cd dev2

## Set Up a Virtual Environment
python -m venv venv
venv\Scripts\activate

## Install Dependencies
pip install -r requirements.txt

## Apply Database Migrations
python manage.py makemigrations
python manage.py migrate

## Create a Superuser
python manage.py createsuperuser

## Run the Development Server
python manage.py runserver

- Access the Application
- Open your browser and navigate to http://127.0.0.1:8000/
- Use your superuser credentials to log in to the Django admin panel.
