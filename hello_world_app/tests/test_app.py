import pytest
from flask import Flask
from app.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    rv = client.get('/')
    assert rv.status_code == 200

def test_analyze_empty_input(client):
    rv = client.post('/analyze', json={})
    assert rv.status_code == 400

def test_analyze_valid_text(client):
    rv = client.post('/analyze', json={
        'type': 'text',
        'data': 'This is a sample privacy policy.'
    })
    assert rv.status_code == 200

def test_analyze_invalid_url(client):
    rv = client.post('/analyze', json={
        'type': 'url',
        'data': 'not-a-url'
    })
    assert rv.status_code == 400