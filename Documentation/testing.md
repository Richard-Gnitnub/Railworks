### **Testing Documentation**

#### **Purpose**
This document outlines the testing strategy, tools, and processes used in the Lightweight Track Builder project. The aim is to ensure robust, reliable, and maintainable code through structured testing and continuous integration.

---

### **Testing Tools and Frameworks**

1. **Coverage**
   - **Purpose**: Measure code coverage for tests.
   - **Usage**:
     - Install using `pip install coverage`.
     - Run tests with coverage tracking:
       ```bash
       coverage run manage.py test
       ```
     - View coverage report:
       ```bash
       coverage report
       ```
     - Generate HTML report:
       ```bash
       coverage html
       ```

2. **Codecov**
   - **Purpose**: Visualise and track test coverage.
   - **Integration**:
     - Upload coverage reports using the bash uploader:
       ```bash
       bash <(curl -s https://codecov.io/bash) -t <your_codecov_token>
       ```
     - Verify uploads on the Codecov dashboard.

3. **pytest**
   - **Purpose**: Run and manage test cases.
   - **Usage**:
     - Install using `pip install pytest`.
     - Run tests:
       ```bash
       pytest
       ```

4. **Ruff**
   - **Purpose**: Perform linting and enforce coding standards.
   - **Usage**:
     - Install using `pip install ruff`.
     - Run Ruff locally:
       ```bash
       ruff .
       ```

5. **GitHub Actions**
   - **Purpose**: Automate testing and linting in CI/CD pipeline.
   - **Usage**:
     - Define workflows in `.github/workflows/main.yml`:
       ```yaml
       name: CI/CD
       on:
         push:
           branches:
             - main
       jobs:
         test:
           runs-on: ubuntu-latest
           steps:
             - name: Checkout code
               uses: actions/checkout@v3
             - name: Set up Python
               uses: actions/setup-python@v4
               with:
                 python-version: '3.10'
             - name: Install dependencies
               run: pip install -r requirements.txt
             - name: Run tests
               run: pytest
             - name: Run coverage
               run: coverage run manage.py test && coverage report
             - name: Upload to Codecov
               run: bash <(curl -s https://codecov.io/bash) -t ${{ secrets.CODECOV_TOKEN }}
       ```

---

### **Testing Workflow**

1. **Local Testing**
   - Run tests locally using `pytest` to validate functionality.
   - Check code coverage with `coverage`.
   - Fix any failing tests or reduce untested code paths.

2. **Continuous Integration**
   - Push changes to the repository to trigger GitHub Actions workflows.
   - Automated steps include:
     - Installing dependencies.
     - Running tests with `pytest`.
     - Measuring coverage and uploading results to Codecov.
     - Running Ruff to check for linting issues.

3. **Error Monitoring**
   - Monitor errors using Sentry to identify runtime issues not covered by tests.

---

### **Writing Test Cases**

1. **Structure**
   - Use `pytest` for all test cases.
   - Place test files in the `tests/` directory.
   - Follow naming conventions: `test_<module_name>.py`.

2. **Example Test**
   ```python
   import pytest
   from trackbuilder_app.models import Gauge

   @pytest.mark.django_db
   def test_gauge_creation():
       gauge = Gauge.objects.create(name="OO-BF", width=16.5)
       assert gauge.name == "OO-BF"
       assert gauge.width == 16.5
   ```

3. **Test Coverage**
   - Ensure tests cover all critical functionality, including:
     - Model validations.
     - View logic.
     - API endpoints.
     - Edge cases.

---

### **Troubleshooting Common Issues**

1. **Tests Failing Locally but Passing in CI**
   - Ensure local environment mirrors CI setup (Python version, dependencies).
   - Check for missing environment variables.

2. **Low Coverage**
   - Identify untested areas using `coverage report`.
   - Write additional tests to cover these areas.

3. **Linting Errors**
   - Run `ruff .` to identify and fix linting issues.
   - Configure `ruff` rules in `pyproject.toml` for project-specific standards.

---

### **Future Enhancements**

- Add end-to-end tests for user interactions.
- Integrate browser-based testing with tools like Selenium or Playwright.
- Expand test coverage for edge cases and exceptional scenarios.


