import pytest
from app import create_app, db

@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_get_products(client):
    response = client.get('/api/products/')
    assert response.status_code == 200
