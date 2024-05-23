import pytest
from flask import json
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import *  # Assuming your Flask app is in app.py

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['JWT_SECRET_KEY'] = 'test_secret_key'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
        db.session.remove()
        db.drop_all()

def register_user(client, username, password):
    return client.post('/register', data=json.dumps({
        'username': username,
        'password': password
    }), content_type='application/json')

def login_user(client, username, password):
    return client.post('/login', data=json.dumps({
        'username': username,
        'password': password
    }), content_type='application/json')

def test_register(client):
    response = register_user(client, 'testuser', 'testpassword')
    assert response.status_code == 200
    assert response.get_json() == {'message': 'User registered successfully'}

def test_login(client):
    register_user(client, 'testuser', 'testpassword')
    response = login_user(client, 'testuser', 'testpassword')
    assert response.status_code == 200
    assert 'token' in response.get_json()

def test_invalid_login(client):
    register_user(client, 'testuser', 'testpassword')
    response = login_user(client, 'testuser', 'wrongpassword')
    assert response.status_code == 401
    assert response.get_json() == {'message': 'Invalid credentials'}

def test_add_task(client):
    register_user(client, 'testuser', 'testpassword')
    login_response = login_user(client, 'testuser', 'testpassword')
    token = login_response.get_json()['token']

    response = client.post('/api/tasks', data=json.dumps({
        'description': 'Test Task'
    }), content_type='application/json', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data['message'] == 'Task added successfully' 

def test_get_tasks(client):
    register_user(client, 'testuser', 'testpassword')
    login_response = login_user(client, 'testuser', 'testpassword')
    token = login_response.get_json()['token']

    client.post('/api/tasks', data=json.dumps({
        'description': 'Test Task'
    }), content_type='application/json', headers={'Authorization': f'Bearer {token}'})

    response = client.get('/api/tasks', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    tasks = response.get_json()
    assert len(tasks) == 1
    assert tasks[0]['description'] == 'Test Task'

def test_delete_task(client):
    register_user(client, 'testuser', 'testpassword')
    login_response = login_user(client, 'testuser', 'testpassword')
    token = login_response.get_json()['token']

    post_response = client.post('/api/tasks', data=json.dumps({
        'description': 'Test Task'
    }), content_type='application/json', headers={'Authorization': f'Bearer {token}'})
    
    task_id = post_response.get_json()['data']['id']
    
    delete_response = client.delete(f'/api/tasks/{task_id}', headers={'Authorization': f'Bearer {token}'})
    assert delete_response.status_code == 200
    assert delete_response.get_json() == {'message': 'Task deleted successfully'}

    get_response = client.get('/api/tasks', headers={'Authorization': f'Bearer {token}'})
    assert get_response.status_code == 200
    tasks = get_response.get_json()
    assert len(tasks) == 0

def test_check_db(client):
    response = client.get('/check_db')
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Database connection successful'}
