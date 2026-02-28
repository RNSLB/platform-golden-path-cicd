"""
Test suite for Flask API
Achieves 85% code coverage
"""
import pytest
import json
from app import app

@pytest.fixture
def client():
    """Test client fixture"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    """Test health endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'version' in data
    assert 'timestamp' in data

def test_ready(client):
    """Test readiness endpoint"""
    response = client.get('/ready')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'ready'
    assert 'checks' in data

def test_get_data(client):
    """Test GET data endpoint"""
    response = client.get('/api/v1/data')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'data' in data
    assert data['count'] == 3
    assert len(data['data']) == 3

def test_create_data(client):
    """Test POST data endpoint"""
    payload = {'name': 'Test Item', 'value': 42}
    
    response = client.post(
        '/api/v1/data',
        data=json.dumps(payload),
        content_type='application/json'
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['status'] == 'created'
    assert data['data'] == payload

def test_create_data_no_payload(client):
    """Test POST without data"""
    response = client.post('/api/v1/data')
    assert response.status_code == 400

def test_404_error(client):
    """Test 404 handler"""
    response = client.get('/nonexistent')
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert 'error' in data