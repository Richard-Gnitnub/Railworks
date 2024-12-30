# How to Contribute

This guide outlines the steps for contributing to the project using GitHub commands. It covers cloning the repository, creating branches, making changes, committing updates, and submitting pull requests.

---

## Prerequisites

Before contributing, ensure you have the following:
1. **Git Installed**: Install Git if not already installed. [Download Git](https://git-scm.com/downloads).
2. **GitHub Account**: Create an account on [GitHub](https://github.com).
3. **Access to the Repository**: Ensure you have access to the project repository.

---

## Contribution Workflow

### Step 1: Fork the Repository

To keep the original repository clean, fork it into your GitHub account:
```bash
# Open the repository in your browser and click "Fork".
Step 2: Clone the Forked Repository
Clone your forked repository to your local machine:
```
```bash
Copy code
git clone https://github.com/your-username/railworks.git
cd railworks
Step 3: Set Up the Upstream Repository
Set the original repository as the upstream remote:
```
```bash
Copy code
git remote add upstream https://github.com/original-owner/railworks.git
git remote -v
This ensures you can sync updates from the original repository.
```
### Step 4: Create a Branch
Create a new branch for your feature or bug fix:

```bash
Copy code
git checkout -b feature/new-feature
```
Use a descriptive branch name that reflects the purpose of your changes.

### Step 5: Make Changes
Make your changes to the codebase using your preferred editor or IDE. Ensure your changes:

Follow the project's coding standards.
Pass all existing tests.
Include new tests for any added functionality.
### Step 6: Stage and Commit Changes
Stage your changes for commit:

```bash
Copy code
git add .
Commit your changes with a descriptive message:
```
```bash
Copy code
git commit -m "Add feature: detailed description of the feature or fix"
```
### Step 7: Push Changes to Your Fork
Push your branch to your forked repository on GitHub:

```bash
Copy code
git push origin feature/new-feature
```
### Step 8: Open a Pull Request
Go to your forked repository on GitHub.
Navigate to the branch you pushed.
Click on Compare & Pull Request.
Provide a clear title and description of your changes.
Submit the pull request.
### Step 9: Respond to Feedback
Collaborators may review your pull request and provide feedback. Make additional commits to your branch if required:

```bash
Copy code
# Make changes
git add .
git commit -m "Address feedback: specific changes made"
git push origin feature/new-feature
```
---
## Keeping Your Fork Up-to-Date
### To sync your fork with the original repository:

```bash
Copy code
# Fetch updates from the upstream repository
git fetch upstream

# Switch to the main branch
git checkout main

# Merge updates into your branch
git merge upstream/main
If there are conflicts, resolve them before proceeding.
```
---

## Best Practices
1. Work on a Branch: Always create a new branch for your work.
2. Write Clear Commit Messages: Use descriptive and concise commit messages.
3. Run Tests Locally: Ensure all tests pass before submitting a pull request.
4. Keep Pull Requests Focused: Submit pull requests for a single feature or fix.

## Summary
```bash
# Fork the Repository
# (This step is done via the GitHub website. Fork the repository to your GitHub account.)

# Clone the Forked Repository
git clone https://github.com/your-username/railworks.git
cd railworks

# Set Up the Upstream Repository
git remote add upstream https://github.com/original-owner/railworks.git
git remote -v

# Create a Branch
git checkout -b feature/new-feature

# Make Changes (Edit files using your preferred editor or IDE)

# Stage and Commit Changes
git add .
git commit -m "Add feature: detailed description of the feature or fix"

# Push Changes to Your Fork
git push origin feature/new-feature

# Sync Your Fork with Upstream Repository (if needed)
git fetch upstream
git checkout main
git merge upstream/main

# Resolve Merge Conflicts (if necessary), then continue pushing changes
git add .
git commit -m "Resolve merge conflicts"
git push origin main
```