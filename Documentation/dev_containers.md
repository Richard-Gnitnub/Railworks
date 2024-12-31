Development Containers (Dev Containers) Documentation

Overview

Development containers, or "dev containers," provide a consistent development environment using Docker. This approach avoids "it works on my machine" issues and ensures reproducibility across setups.

For the Lightweight Track Builder project, we use dev containers to streamline the development and testing of our Django application.

Features

Preconfigured Environment: Includes Python, Django, CadQuery, and necessary dependencies.

Isolation: Runs independently of your local environment.

Cross-platform: Works on any machine with Docker and Visual Studio Code.

Pre-installed Tools: Linter, debugger, and other tools for Python/Django development.

Prerequisites

Docker: Ensure Docker Desktop is installed and running.

Visual Studio Code: Install VS Code.

Dev Containers Extension: Install the "Dev Containers" extension in VS Code.

Setting Up the Dev Container

1. Add Dev Container Configuration

Create a .devcontainer directory in the root of your project with the following files:

a. devcontainer.json
```json
{
  "name": "Django Dev Container",
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

b. Dockerfile
```bash

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

2. Start the Dev Container

Open your project in VS Code.

Use the Command Palette (Ctrl+Shift+P) to select Reopen in Container.

Using the Dev Container

Running the Django Server

Once inside the container:

Activate the container terminal.

Run the server:

python manage.py runserver 0.0.0.0:8000

Access the app via http://localhost:8000.

Testing in the Dev Container

Run unit tests with:

python manage.py test

Validate STL file generation:

python manage.py generate_stl

Customising the Dev Container

You can modify the Dockerfile or devcontainer.json to include additional tools or configurations specific to your workflow.

Troubleshooting

Docker Daemon Not Running:
Ensure Docker Desktop is running before opening the dev container.

Dependencies Not Installed:
Check the postCreateCommand in devcontainer.json for accuracy.

Port Binding Issues:
Ensure no other service is using port 8000 or change it in devcontainer.json and manage.py runserver.