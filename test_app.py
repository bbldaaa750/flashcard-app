import pytest
from app import create_app
from app.extensions import db
from config import TestConfig

@pytest.fixture
def app():
    app = create_app(config_class=TestConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_homepage(client):
    response = client.get('/', follow_redirects=True)
    assert response.status_code == 200
