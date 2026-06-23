# --- Build Stage ---
FROM python:3.12-slim-bookworm AS builder

# Install uv for fast dependency installation
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Enable bytecode compilation for faster import performance
ENV UV_COMPILE_BYTECODE=1

# Copy package config files
COPY pyproject.toml uv.lock ./

# Install dependencies (exclude dev dependencies and skip installing project itself for caching)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project


# --- Runtime Stage ---
FROM python:3.12-slim-bookworm AS runner

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Prepend virtual env bin folder to path
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Copy source code and config files
COPY src/ ./src
COPY pyproject.toml README.md ./

# Install the application itself into virtual environment without reinstating dependencies
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
RUN uv pip install --no-deps .
RUN rm /bin/uv /bin/uvx

# Create logs directory and configure non-root security container privileges
RUN mkdir -p /app/logs && chown -R 10001:10001 /app

EXPOSE 8000

USER 10001

# Run the FastAPI server using the CLI script entrypoint
CMD ["base_fast_api", "--host", "0.0.0.0", "--port", "8000"]
