```markdown
# Setting Up Dev Containers for the Lightweight Track Builder Project

### **Step 1: Verify Prerequisites**
Make sure you have:

1. **Docker Desktop** installed and running.
2. **Visual Studio Code (VS Code)** installed.
3. **Dev Containers Extension** installed in VS Code:
   - Search for "Dev Containers" in the Extensions Marketplace and install it.

---

### **Step 2: Create Dev Container Configuration**

In your project directory, create a folder named `.devcontainer` and add two files:

#### a. **`devcontainer.json`**

This file defines the configuration for your dev container.

```json
{
  "name": "Lightweight Track Builder",
  "dockerFile": "Dockerfile",
  "context": "..",
  "settings": {
    "python.defaultInterpreterPath": "/usr/local/bin/python",
    "editor.formatOnSave": true
  },
  "extensions": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "esbenp.prettier-vscode"
  ],
  "postCreateCommand": "pip install -r requirements.txt && python manage.py migrate",
  "remoteUser": "vscode",
  "forwardPorts": [8000],
  "mounts": [
    "source=${localWorkspaceFolder},target=/workspace,type=bind,consistency=cached"
  ],
  "workspaceFolder": "/workspace"
}
```

#### b. **`Dockerfile`**

This file specifies the environment your project needs:

```dockerfile
# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /workspace/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Default command
CMD ["bash"]
```

---

### **Step 3: Open Project in a Dev Container**

1. Open your project folder in **VS Code**.
2. Use the Command Palette (`Ctrl+Shift+P` or `Cmd+Shift+P`) and select **Reopen in Container**.
3. VS Code will build the container using the provided **Dockerfile** and set up your environment.

---

### **Step 4: Run the Django Server**

1. Inside the container terminal, activate the development server:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```
2. Access the application at `http://localhost:8000`.

---

### **Step 5: Test Functionality**

- Run unit tests:
  ```bash
  python manage.py test
  ```
- Validate STL file generation:
  ```bash
  python manage.py generate_stl
  ```

---

### **Step 6: Customising the Container**

If you need additional dependencies or configurations (e.g., specific testing tools, extra libraries), modify the **Dockerfile** or **devcontainer.json** accordingly. Rebuild the container to apply changes by selecting **Rebuild Container** in the Command Palette.

---

This guide provides a complete setup for using dev containers in your Django project.
```

