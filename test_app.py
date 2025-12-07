import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True 
    with app.test_client() as client:
        yield client

def test_homepage(client):
    response = client.get('/', follow_redirects=True)
    assert response.status_code == 200
