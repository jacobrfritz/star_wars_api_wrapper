from fastapi import FastAPI
from star_wars_api_wrapper.main import create_app


def test_create_app() -> None:
    """Verifies that the factory function successfully instantiates
    a FastAPI application.
    """
    app = create_app()
    assert isinstance(app, FastAPI)
    assert app.title == "FastAPI Base Service"
