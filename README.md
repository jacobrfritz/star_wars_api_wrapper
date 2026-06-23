# base_fast_api

A production-ready, highly flexible, and containerized FastAPI template using `uv` for lightning-fast dependency management and packaging.

This template provides all the boilerplate and baseline architectural setups required to quickly spin up a solid web service or microservice.

---

## Key Features

- **Fast Dependency Syncing**: Utilizes [uv](https://github.com/astral-sh/uv) to manage, resolve, and lock dependencies in milliseconds.
- **Structured JSON & Colored Console Logging**: Features a robust, pre-configured logging subsystem that writes human-readable colored logs to `stdout` (console) and machine-readable structured JSON to files under `logs/app.log` with automatic rotation.
- **Request Tracing (Correlation ID)**: Middleware automatically extracts or generates a unique correlation ID (`X-Correlation-ID`) for every request, injecting it into all log statements triggered during that request context and returning it in headers.
- **Unified Error Handling**: Includes global handlers mapping custom validation messages and user exceptions into consistent, typed JSON response schemas.
- **Environment-based Configuration**: Settings are parsed from `.env` files using `pydantic-settings` with type verification.
- **API Versioning & CRUD Boilerplate**: Pre-configured router setups (under `/api/v1`) with mock items CRUD endpoints and health check endpoints.
- **Testing Architecture**: Test clients and settings overrides configured in `tests/conftest.py` with 100% passing tests for routing, tracing, error handling, and logger structures.
- **Dockerization**: Optimized multi-stage `Dockerfile` with bytecode compilation, dependencies caching, and root privilege separation, plus a `docker-compose.yml` local hot-reload profile.

---

## Setup & Bootstrap

This template features a bootstrapping script to quickly rename the project and set up your development environment.

To bootstrap your own service from this template, run:

```bash
python bootstrap.py
```

The bootstrap script will:
1. **Check for `uv`**: Automatically installs `uv` locally if not present.
2. **Rename Project**: Guides you through choosing a name (e.g., `my_awesome_service`) and renaming the package imports, Makefile references, and script paths.
3. **Sync Dependencies**: Installs project dependencies.
4. **Pre-commit setup**: Registers Ruff and MyPy hooks.

---

## Usage

Common development tasks can be run using the provided `Makefile` or directly via `uv`.

### Development Commands

| Task | Make Command | Direct `uv` Command | Description |
| :--- | :--- | :--- | :--- |
| **Sync Dependencies** | `make install` | `uv sync` | Install or sync dependencies. |
| **Run API Web Server** | `make run` | `uv run base_fast_api --reload` | Run the application with auto-reloading. |
| **Run Test Suite** | `make test` | `uv run pytest` | Run all test suites. |
| **Watch Tests** | `make test-watch` | `uv run ptw` | Watch files and run tests on save. |
| **Coverage Report** | `make test-cov` | `uv run pytest --cov=src --cov-report=term-missing` | Run tests with coverage output. |
| **Lint Check** | `make lint` | `uv run ruff check .` | Check style issues with Ruff. |
| **Format Code** | `make format` | `uv run ruff format .` | Format files. |
| **Type Check** | `make typecheck` | `uv run mypy src` | Check static types with MyPy. |

Once the server is running, visit **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)** to interact with the Swagger UI documentation.

---

## Project Structure

```text
.
├── .dockerignore
├── .editorconfig
├── .gitignore
├── .pre-commit-config.yaml
├── Dockerfile
├── Makefile
├── README.md
├── bootstrap.py
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
├── src/
│   └── base_fast_api/
│       ├── __init__.py
│       ├── api/
│       │   └── v1/
│       │       ├── endpoints/
│       │       │   ├── health.py
│       │       │   └── items.py
│       │       └── router.py
│       ├── cli.py
│       ├── config.py
│       ├── core/
│       │   └── exceptions.py
│       ├── logger.py
│       ├── middleware/
│       │   └── correlation_id.py
│       └── main.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_api.py
    ├── test_bootstrap.py
    ├── test_logger.py
    └── test_main.py
```

- `src/base_fast_api/config.py`: Application config definitions using Pydantic Settings.
- `src/base_fast_api/core/exceptions.py`: Custom HTTP application exceptions and error-formatting handlers.
- `src/base_fast_api/middleware/correlation_id.py`: Tracing middleware attaching `X-Correlation-ID` to logs and requests.
- `src/base_fast_api/api/`: Endpoint definitions separated by versions.
- `tests/conftest.py`: Shared pytest client configuration and overrides.
