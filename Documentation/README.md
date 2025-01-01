[![codecov](https://codecov.io/github/Richard-Gnitnub/Railworks/graph/badge.svg?token=WFXJ7Y2KVE)](https://codecov.io/github/Richard-Gnitnub/Railworks)

# **PROJECT**:
**Lightweight Track Builder**

---

## **GOAL**
Develop a lightweight Django-based application to design accurate model railway track for 3D printing, focusing on **COT (Chairs on Timbers) track**. This MVP prioritises straight track generation adhering to bullhead rail standards based on REA specifications. The generated STL files include timbers with integrated chairs, and the rail will be manually added post-printing. The MVP serves as a foundation for a modular and extensible track design tool.

---

## **CURRENT CAPABILITIES**
- **Framework**: Established Django project with core application structure.
- **Testing**:
  - Using **pytest** and **Factory Boy** for unit tests and test data generation.
  - **Ruff** integrated for linting and maintaining code consistency.
- **Database**:
  - Migrated key models (‘Track’, ‘Gauge’, ‘BullheadChairs’) to Django ORM.
  - Relationships tested and verified.
- **UI/UX**:
  - Implemented DaisyUI in the admin interface.
- **CI/CD**:
  - Basic pipeline setup with Docker Cloud for automated builds and testing in a SQLite environment.

---

## **ASPIRATIONAL GOALS**
- **Testing Enhancements**:
  - Add integration tests for Django-CadQuery interactions.
  - Incorporate API tests and regression testing.
  - Expand edge-case validations for track parameters and geometry configurations.
- **Deployment Improvements**:
  - Transition to PostgreSQL for production scalability.
  - Expand CI/CD to include automated regression tests and staging pipelines.
- **STL Validation**:
  - Integrate STL integrity checks and provide automated feedback through Django views.
  - Include geometry visualisation tools for user-friendly validation.

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
- Build the MVP using **Django** for its robust ORM, admin interface, REST API, and scalability.

### **Core Features**
- **STL Generation**:
  - Parameterised straight plain track geometry using REA Bullhead standards.
- **Database Integration**:
  - Models for dynamic track configurations stored in SQLite.
- **Admin Panel**:
  - Manage CRUD operations for timbers, chairs, gauges, and track settings, styled with DaisyUI.

### **Excluded from MVP**
- **Flat Bottom Rail**
- **Curved Tracks** and **Turnouts**
- **Highly Detailed Plug Tracks**
- **Mesh Inspection and Repair**

---

## **WORKING ENVIRONMENT REQUIREMENTS**
- **Development Tools**:
  - Python 3.10+
  - PIP package manager
  - Django 5.x
  - Docker for containerisation
  - Factory Boy for test data generation
  - Ruff for linting
- **Development Environment**:
  - IDE: Visual Studio Code
  - CLI: Command Prompt (Windows)
  - Version Control: GitHub Desktop
- **Database**:
  - SQLite for development

---

## **TESTING FRAMEWORK**
Currently, testing is conducted using **pytest** in conjunction with **Factory Boy** for generating robust test data. We prioritise:
- Unit tests for database models to ensure data integrity.
- Geometry validation tests for key STL generation scripts.

**Ruff** is integrated into the development workflow to ensure code consistency and adherence to Python coding standards.

**Aspirational Goals**:
- Expand test coverage to include:
  - Integration tests for validating Django-CadQuery interactions.
  - API tests to ensure reliable communication between the front end and back end.
  - Edge-case validations for track parameters and geometry configurations.
- Automate test execution and validation via a CI/CD pipeline.
- Add support for regression testing to prevent errors in iterative development.
- Incorporate STL integrity checks directly into the testing framework.

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

## **SETUP INSTRUCTIONS**

### Clone the Repository
```
git clone <repository-url>
cd dev2
```

### Set Up a Virtual Environment
```
python -m venv venv
venv\Scripts\activate
```

### Install Dependencies
```
pip install -r requirements.txt
```

### Apply Database Migrations
```
python manage.py makemigrations
python manage.py migrate
```

### Create a Superuser
```
python manage.py createsuperuser
```

### Run the Development Server
```
python manage.py runserver
```

- Access the Application: Open your browser and navigate to `http://127.0.0.1:8000/`
- Use your superuser credentials to log in to the Django admin panel.

