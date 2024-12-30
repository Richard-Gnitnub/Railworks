# CI/CD Pipeline Documentation

This document outlines the complete setup, workflow, and troubleshooting for our CI/CD pipeline. It supports deployments through both the **CLI** and the **Docker Desktop App**, ensuring consistency and reliability across environments.

---

## Pipeline Overview

### Stages

1. **Test and Validate**:
    - Lint the codebase.
    - Run unit tests and migrations to ensure code quality.

2. **Deploy to Staging**:
    - Build and push Docker images tagged for staging.
    - Deploy the staging image to Docker Cloud.

3. **Deploy to Production**:
    - Build and push Docker images tagged for production.
    - Deploy the production image to Docker Cloud.

### Key Features

- Multi-platform builds using Docker Buildx.
- Layer caching for efficient builds.
- Automated deployment to Docker Cloud on `staging` and `main` branches.
- Vulnerability scanning using Docker Scout.

---

## Using the CLI

### Setup Buildx

To set up Docker Buildx with the cloud driver:

```bash
# Set up Buildx with cloud driver
docker buildx create --name cloud-builder --driver cloud --use
```

## Build and Push Commands

### Staging Deployment:

```bash
# Build and push to staging
docker buildx build --platform linux/amd64,linux/arm64 \
  --push -t username/railworks:staging .
```

### Production Deployment

```bash
# Build and push to production
docker buildx build --platform linux/amd64,linux/arm64 \
  --push -t username/railworks:latest .
```

## Cach Optimisation

to use caching for faster builds:
```bash
--cache-from=type=registry,ref=username/railworks:cache \
--cache-to=type=inline,push=true
```
## Docker Scout for Vulnerabilites
```bash
--cache-from=type=registry,ref=username/railworks:cache \
--cache-to=type=inline,push=true
```
---

## Using the Docker Desktop App

1. Open **Docker Desktop** and navigate to the **images** tab
2. Use the search bar to locate `railworks` images
3. Verify that the `staging` and `latest` tags are up-to-date.
4. For manual deployments:
    - Go to the **containers/Apps** tab.
    - Start or redeploy the container using the latest image.
## Troubleshooting in Docker Desktop
1. Check the container logs for errors.
2. Verigy the image tag matches the environment (eg., `staging` or `latest`).
3. Ensure Docker Desktop is connected to Docker Cloud if using automated builds.
---
## GitHub Actions Workflow
### Trigger Points
- Staging Deployment: Triggered on pushes to the staging branch.
- Production Deployment: Triggered on merges to the main branch.
## Workflow Configuration
## Test and Validate:
```bash
- name: Run Unit Tests
  run: pytest

- name: Run Linter
  run: ruff check .

```
### Build and Push:


```yaml
- name: Build and Push Docker Image
  uses: docker/build-push-action@v5
  with:
    context: .
    push: true
    tags: |
      username/railworks:staging
      username/railworks:${{ github.sha }}
    platforms: linux/amd64,linux/arm64
```
---
## Troubleshooting CI/CD Issues
### Common Errors and Solutions
1. **Image Not Pushed**:

    -Ensure push: true is set in docker/build-push-action.
    -Verify Docker credentials (DOCKER_USER, DOCKER_PAT) are correctly configured in GitHub Secrets.
2. **Buildx Warnings**:

    -Add `--push` to the `docker buildx build` command to ensure images are pushed to the registry.
3. **Cache Issues**:

    -Check that `cache-from` and `cache-to` options are correctly set for Docker caching.
4. **Deployment Errors**:

    -Ensure the correct image tag is used in the deployment (e.g., `staging`, `latest`).
    -Verify network connectivity to Docker Cloud.
---
## Best Practices
1. **Automate Deployments**:

    -Use GitHub Actions to automate the CI/CD pipeline for consistency and efficiency.
2. **Monitor Builds**:

    -Regularly check logs in Docker Cloud and GitHub Actions for warnings or errors.
3. **Secure Your Pipeline**:

    -Use `GITHUB_TOKEN` and encrypted secrets for authentication.
4. **Document Changes**:

    -Update this document as the pipeline evolves.