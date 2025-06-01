# CHANGELOG


## v0.3.0 (2025-06-01)

### Chores

- Update project URLs in pyproject.toml and README, bump version to 0.2.1
  ([`81be805`](https://github.com/RYZHAIEV-SERHII/job-search-ai-assistant/commit/81be8057895009f0b13b72bef0bec979661a5067))

### Features

- Add Crawl4AI integration for job scraping
  ([`0831220`](https://github.com/RYZHAIEV-SERHII/job-search-ai-assistant/commit/083122034f16bf6e3f4c8ba5b32bb1aee398004f))

- Add JobPosting schema and validation tests
  ([`646eb83`](https://github.com/RYZHAIEV-SERHII/job-search-ai-assistant/commit/646eb831a77a517c54ced4b25da1218abfd7c16b))

Introduce the JobPosting schema for standardized job data and add robust validation logic, including
  URL and requirements validation. Implement a comprehensive test suite to verify schema
  functionality, covering optional defaults, invalid inputs, and edge cases for data validation.

- Add LLM-based extraction strategy for job listings
  ([`86e45f6`](https://github.com/RYZHAIEV-SERHII/job-search-ai-assistant/commit/86e45f6a7fdfec0747d1228e5eeb7faa542a579c))

- Add platform adapters for job search sites
  ([`efd1e14`](https://github.com/RYZHAIEV-SERHII/job-search-ai-assistant/commit/efd1e14fba985e8a3f014dea8dd61cc63c9cc88c))

- Enhance job search API schemas and update references to SearchFilters
  ([`2d842d0`](https://github.com/RYZHAIEV-SERHII/job-search-ai-assistant/commit/2d842d0e08892b2bae7e3da907b90e1e2a5ba70e))

### Refactoring

- Reorganize application structure and improve test configuration
  ([`e040a2d`](https://github.com/RYZHAIEV-SERHII/job-search-ai-assistant/commit/e040a2d5fc2b39c1d070b6a806e36368dc4c13e2))

- Update field validators to use classmethod decorator in Pydantic models
  ([`1b05ff5`](https://github.com/RYZHAIEV-SERHII/job-search-ai-assistant/commit/1b05ff525aee001d6374053e350b2340c9356076))

- Update type hints to use PEP 604 syntax and enhance model validation
  ([`9a5c2ff`](https://github.com/RYZHAIEV-SERHII/job-search-ai-assistant/commit/9a5c2ff06924ac95c6c2d2c1294a83ab5932c4c0))

### Testing

- Add comprehensive tests for Crawl4AI JobPosting model validation
  ([`ec378a2`](https://github.com/RYZHAIEV-SERHII/job-search-ai-assistant/commit/ec378a28ffeaff8d85b5d340d0ce422c0f558566))

- Add comprehensive tests for JobScraperClient with filtering and fallback scenarios
  ([`7d724e2`](https://github.com/RYZHAIEV-SERHII/job-search-ai-assistant/commit/7d724e2e0848d53c73b60b422c49709a88f82bf7))

- Add comprehensive tests for search API schemas
  ([`c925d6f`](https://github.com/RYZHAIEV-SERHII/job-search-ai-assistant/commit/c925d6f5a851944a84240178206fe654202d4623))

- Add unit tests for crawl4ai exceptions module
  ([`964451e`](https://github.com/RYZHAIEV-SERHII/job-search-ai-assistant/commit/964451ee2d88de0669d1204df836822d6fe38720))

- Enhance test coverage for job collectors and platform adapters
  ([`1d11460`](https://github.com/RYZHAIEV-SERHII/job-search-ai-assistant/commit/1d11460930ccf12673005ca596a660d22b50a4d6))

- Enhance test coverage for JobLLMExtractionStrategy with retry and fallback scenarios
  ([`360cb58`](https://github.com/RYZHAIEV-SERHII/job-search-ai-assistant/commit/360cb58e2939f71eb669d81dd8bfc0b673b5af8a))

- Reformat unit tests for job platform adapters into separate files.
  ([`3761a12`](https://github.com/RYZHAIEV-SERHII/job-search-ai-assistant/commit/3761a12682cdd0fb85b83dbde1c339d2c780d1d2))


## v0.2.1 (2025-05-25)

### Bug Fixes

- Add httpx dependency so the quality-check workflow works properly.
  ([`e9f295e`](https://github.com/RYZHAIEV-SERHII/job-search-ai-assistant/commit/e9f295e98730b9e1ae30755f3886c19a7cc24b2b))


## v0.2.0 (2025-05-25)

### Documentation

- Update documentation for Job Search AI Assistant
  ([`22e43cb`](https://github.com/RYZHAIEV-SERHII/job-search-ai-assistant/commit/22e43cbee6829360bf269785555306155cfbea9e))

### Features

- Add test configuration and fixtures, implement tests for application and health check
  ([`a6ca11f`](https://github.com/RYZHAIEV-SERHII/job-search-ai-assistant/commit/a6ca11fa04c8ddd1a2d19b1da8be118ad10318d9))


## v0.1.0 (2025-05-25)

### Chores

- Update dependencies and configuration files.
  ([`0635622`](https://github.com/RYZHAIEV-SERHII/job-search-ai-assistant/commit/063562227addce79a188124a6b2ee5a0cab4e6fa))

### Features

- Add FastAPI integration with health check and API setup
  ([`4bc6357`](https://github.com/RYZHAIEV-SERHII/job-search-ai-assistant/commit/4bc6357f7fb38165b18fe88f68a1e09bcf74288d))

Introduced FastAPI application with health check endpoint and modular API structure. Included
  configurations, schema, and middleware for error handling, CORS, and gzip compression. Updated the
  main entry point to run the API using Uvicorn.


## v0.0.0 (2025-05-24)

### Chores

- Setup project structure and workflow
  ([`7294b18`](https://github.com/RYZHAIEV-SERHII/job-search-ai-assistant/commit/7294b182102bf88bfc2de53caae89144f8598213))

### Documentation

- Updated README.md and other documentation.
  ([`0877120`](https://github.com/RYZHAIEV-SERHII/job-search-ai-assistant/commit/087712008fd1dc6f367596693e9ba3abf01c507b))
