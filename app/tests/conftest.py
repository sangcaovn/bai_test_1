import pytest

from app.main import create_app


@pytest.fixture()
def client():
    yield create_app('dev')
