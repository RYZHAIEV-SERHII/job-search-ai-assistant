# job-search-ai-assistant

[![Release](https://img.shields.io/github/v/release/RYZHAIEV-SERHII/job-search-ai-assistant)](https://img.shields.io/github/v/release/RYZHAIEV-SERHII/job-search-ai-assistant)
[![Build status](https://img.shields.io/github/actions/workflow/status/RYZHAIEV-SERHII/job-search-ai-assistant/main.yml?branch=main)](https://github.com/RYZHAIEV-SERHII/job-search-ai-assistant/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/RYZHAIEV-SERHII/job-search-ai-assistant/branch/main/graph/badge.svg)](https://codecov.io/gh/RYZHAIEV-SERHII/job-search-ai-assistant)
[![Commit activity](https://img.shields.io/github/commit-activity/m/RYZHAIEV-SERHII/job-search-ai-assistant)](https://img.shields.io/github/commit-activity/m/RYZHAIEV-SERHII/job-search-ai-assistant)
[![License](https://img.shields.io/github/license/RYZHAIEV-SERHII/job-search-ai-assistant)](https://img.shields.io/github/license/RYZHAIEV-SERHII/job-search-ai-assistant)

This is a template repository for Python projects that use uv for their dependency management.

- **Github repository**: <https://github.com/RYZHAIEV-SERHII/job-search-ai-assistant/>
- **Documentation** <https://RYZHAIEV-SERHII.github.io/job-search-ai-assistant/>

## Getting started with your project

### 1. Create a New Repository

First, create a repository on GitHub with the same name as this project, and then run the following commands:

```bash
git init -b main
git add .
git commit -m "init commit"
git remote add origin git@github.com:RYZHAIEV-SERHII/job-search-ai-assistant.git
git push -u origin main
```

### 2. Set Up Your Development Environment

Then, install the environment and the pre-commit hooks with

```bash
make install
```

This will also generate your `uv.lock` file

### 3. Run the pre-commit hooks

Initially, the CI/CD pipeline might be failing due to formatting issues. To resolve those run:

```bash
uv run pre-commit run -a
```

### 4. Commit the changes

Lastly, commit the changes made by the two steps above to your repository.

```bash
git add .
git commit -m 'Fix formatting issues'
git push origin main
```

You are now ready to start development on your project!
The CI/CD pipeline will be triggered when you open a pull request, merge to main, or when you create a new release.

To finalize the set-up for publishing to PyPI, see [here](https://shaneholloman.github.io/uvi/features/publishing/#set-up-for-pypi).
For activating the automatic documentation with MkDocs, see [here](https://shaneholloman.github.io/uvi/features/mkdocs/#enabling-the-documentation-on-github).
To enable the code coverage reports, see [here](https://shaneholloman.github.io/uvi/features/codecov/).

## Releasing a new version



---

Repository initiated with [shaneholloman/uvi](https://github.com/shaneholloman/uvi).
