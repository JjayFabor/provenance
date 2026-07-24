import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app


@pytest.fixture
def client():
    with patch("app.main.check_connection", return_value=1):
        with TestClient(app) as client:
            yield client