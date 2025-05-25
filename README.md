# Job Search AI Assistant

![Project Logo](https://path-to-your-logo.png)

[![Release](https://img.shields.io/github/v/release/RYZHAIEV-SERHII/job-search-ai-assistant)](https://img.shields.io/github/v/release/RYZHAIEV-SERHII/job-search-ai-assistant)
[![Python 3.9-3.13](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![codecov](https://codecov.io/gh/RYZHAIEV-SERHII/job-search-ai-assistant/branch/main/graph/badge.svg)](https://codecov.io/gh/RYZHAIEV-SERHII/job-search-ai-assistant)
[![Tests](https://github.com/RYZHAIEV-SERHII/job-search-ai-assistant/actions/workflows/quality_checks.yml/badge.svg)](https://github.com/RYZHAIEV-SERHII/job-search-ai-assistant/actions)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://RYZHAIEV-SERHII.github.io/job-search-ai-assistant/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat&logo=github)](CONTRIBUTING.md)

A comprehensive job search aggregator built with Python 3.13 and FastAPI that integrates multiple job platforms to streamline the job hunting process.

---

## ✨ Features

- **Platform Integration**: Connect with multiple job platforms (LinkedIn, Djinni, DOU, Work.ua, and more)
- **Unified Search**: Access all job listings through a single, consistent interface
- **Smart Filtering**: Advanced filtering options to find the most relevant opportunities
- **Notifications**: Customizable email and Telegram notifications for new job listings
- **Analytics Dashboard**: Track job market trends and your application progress

## 🔧 Tech Stack

- **Core Dependencies**
  - Python 3.9-3.13: Full compatibility with multiple Python versions
  - FastAPI: High-performance web framework for building APIs
  - Supabase: Database and authentication backend
  - Streamlit: Interactive web interface
- **Development Tools**
  - Ruff: Fast Python linter and formatter
  - Pre-commit: Automated code quality checks
  - PyTest: Comprehensive test framework with coverage reporting
  - MyPy: Static type checking
  - Tox: Testing across multiple Python environments
  - uv: Fast Python package installer and resolver

## 🚀 Getting Started

### 📋 Prerequisites

- **Python** (3.9-3.13)
- **uv** (0.7.6 or newer)

## 🚀 Installation

1. Clone the repository

    ```bash
    git clone https://github.com/RYZHAIEV-SERHII/job-search-ai-assistant.git
    cd job-search-ai-assistant
    ```

2. Install dependencies using uv

    ```bash
    uv sync
    ```

3. Install pre-commit hooks

    ```bash
    uv run pre-commit install
    uv run pre-commit install --hook-type commit-msg
    ```

4. Run the application

    ```bash
    python main.py
    ```

## 📊 Example Usage

> [!NOTE]
> The project is in early development. Usage examples will be added as features are implemented.

## 🧪 Running Tests

Run tests using Make:

```bash
make test
```

Or directly with pytest:

```bash
pytest
```

To run tests across multiple Python versions:

```bash
tox
```

## 🔍 Code Quality

Run all code quality checks:

```bash
make check
```

This will:

- Check lock file consistency
- Run pre-commit hooks
- Run static type checking with mypy
- Check for obsolete dependencies with deptry

## 📚 Documentation

Build and serve documentation:

```bash
make docs
```

Test if documentation builds without errors:

```bash
make docs-test
```

## 🏗️ Project Structure

```bash
job-search-ai-assistant/
│
├── .github/               # GitHub configuration files
├── .hooks/                # Custom pre-commit hooks
├── docs/                  # Documentation files
├── src/                   # Source code
├── tests/                 # Test files
├── .env                   # Environment variables
├── .gitignore             # Files to ignore in git
├── .pre-commit-config.yaml # Pre-commit configuration
├── CONTRIBUTING.md        # Contributing guidelines
├── Dockerfile             # Docker configuration
├── LICENSE                # License file
├── main.py                # Main entry point
├── Makefile               # Makefile for common tasks
├── mkdocs.yml             # MkDocs configuration
├── pyproject.toml         # Project configuration
├── README.md              # Project documentation
├── tox.ini                # Tox configuration
└── uv.lock                # uv lock file
```

## 🛣️ Roadmap

- [x] Initial project setup
- [x] CI/CD pipeline with GitHub Actions
- [ ] Job platform API integrations
- [ ] Search functionality implementation
- [ ] Notification system
- [ ] Web interface with Streamlit
- [ ] Analytics dashboard

For detailed version history and latest changes, see our [CHANGELOG](CHANGELOG.md) 📈

## 🧰️ Contributing

We welcome contributions! Check out our [Contributing Guidelines](CONTRIBUTING.md).

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 📞 Contact

If you have any questions or suggestions,
feel free to reach out to me at [Email](mailto:rsp89@gmail.com) or [Telegram](https://t.me/CTAJIKEP)

---
Created with ❤️ by [RYZHAIEV-SERHII](https://github.com/RYZHAIEV-SERHII/)
