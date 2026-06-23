from base_fast_api.main import create_app
from fastapi import FastAPI


def test_create_app() -> None:
    """Verifies that the factory function successfully instantiates
    a FastAPI application.
    """
    app = create_app()
    assert isinstance(app, FastAPI)
    assert app.title == "FastAPI Base Service"
