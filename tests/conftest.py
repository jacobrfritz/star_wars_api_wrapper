# Override settings for testing environment before importing app
import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

os.environ["ENV"] = "testing"
os.environ["LOG_FILE"] = ""  # Disable file logging during test runs
os.environ["DEBUG"] = "true"

from star_wars_api_wrapper.main import app  # noqa: E402


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Provides a TestClient for making mock HTTP requests against the FastAPI app."""
    with TestClient(app) as c:
        yield c
