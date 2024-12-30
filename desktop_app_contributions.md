# Contribution Guidelines

Welcome to the project! This document outlines the workflow and best practices for contributing to the application. Following these guidelines will help maintain code quality, streamline development, and ensure smooth deployments.

---

## **Branching Strategy**

The repository uses a structured branching strategy to separate development stages:

1. **Feature Branches**:
   - Name your feature branch descriptively, e.g., `feature/add-login`, `bugfix/fix-api-error`.
   - Work on individual features or fixes in isolated branches.
   - Push changes regularly to the feature branch.

2. **Staging Branch**:
   - After tests pass, merge feature branches into `staging`.
   - Used for integration and staging tests.

3. **Main Branch**:
   - Production-ready code only.
   - Merge into `main` after staging validation is complete.
   - Changes merged into `main` are automatically deployed to production.

---

## **GitHub Desktop Workflow**

1. **Clone the Repository**:
   - Open GitHub Desktop and log in.
   - Navigate to `File > Clone Repository`, and select the repository to clone locally.

2. **Create a New Branch**:
   - From the top bar in GitHub Desktop, click `Current Branch` and select `New Branch`.
   - Name your branch descriptively, e.g., `feature/add-login`, and ensure it is based on the latest `staging` branch.

3. **Develop Locally**:
   - Make code changes in your local environment.
   - Use tools like linters and type checkers for code quality.

4. **Commit Changes**:
   - Stage changes using GitHub Desktop.
   - Add a descriptive commit message, e.g., `feature: add login functionality`.
   - Click `Commit to <branch-name>` to save your changes locally.

5. **Sync and Push Changes**:
   - Once you are ready to share your changes, click `Push Origin` in GitHub Desktop.
   - Your feature branch will now be available on the remote repository.

6. **Open a Pull Request (PR)**:
   - From GitHub Desktop, click `View on GitHub` to navigate to the repository in your browser.
   - Open a pull request against the `staging` branch for review.

---

## **Development Workflow**

1. **Create a Feature Branch**:
   - Ensure your local copy is up-to-date with `staging` using GitHub Desktop or CLI.
   - Create a new branch based on `staging`.

2. **Develop Locally**:
   - Write code and ensure local tests pass.
   - Commit changes using GitHub Desktop.

3. **Push Changes**:
   - Use GitHub Desktop to sync your branch with the remote repository.

4. **Run CI Tests**:
   - Automated tests (unit tests, linters, etc.) will run on the PR.
   - Fix any issues flagged by the CI pipeline.

5. **Merge to Staging**:
   - Once all tests pass and code is reviewed, merge the feature branch into `staging`.

6. **Staging Tests**:
   - Deploy the `staging` branch to the staging environment.
   - Run integration and end-to-end tests.
   - Validate application behavior under near-production conditions.

7. **Merge to Main**:
   - If staging tests pass, merge `staging` into `main`.
   - Deployment to production will be triggered automatically.

---

## **Code Quality Standards**

To maintain a consistent codebase, adhere to the following:

1. **Linting**:
   - Use `flake8` for Python to enforce style consistency.
   - Fix all linting errors before committing.

2. **Type Checking**:
   - Use `mypy` to check for type errors in Python.

3. **Testing**:
   - Write unit tests for all new features.
   - Ensure existing tests pass before submitting a PR.
   - Run tests locally using `pytest`.

4. **Commit Messages**:
   - Use clear, descriptive messages.
   - Format: `<type>: <description>`
     - Example: `feature: add user authentication`

---

## **Pull Request Guidelines**

1. **PR Checklist**:
   - The feature branch is up-to-date with `staging`.
   - Code passes all automated tests.
   - Code has been reviewed.

2. **Review Process**:
   - Reviewers check for code quality, correctness, and adherence to guidelines.
   - Address all comments before merging.

3. **Merge Policy**:
   - Squash commits when merging to keep the history clean.
   - Only merge after all checks pass.

---

By following these enhanced guidelines, including GitHub Desktop usage, you'll help maintain a smooth development process. Thank you for contributing!
