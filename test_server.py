import requests
import pytest
import json

BASE_URL = "http://localhost:8000"

def test_index_page():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert "text/html" in response.headers["Content-Type"]

def test_static_files():
    for file in ["style.css", "script.js"]:
        response = requests.get(f"{BASE_URL}/static/{file}")
        assert response.status_code == 200
        assert file.split(".")[-1] in response.headers["Content-Type"]

def test_valid_json():
    valid_json = json.dumps({
        "project": "JSON Validator",
        "version": "1.0.0",
        "description": "A simple JSON validation service",
        "author": {
            "name": "Your Name",
            "email": "your.email@example.com"
        },
        "dependencies": {
            "python": ">=3.9",
            "docker": "latest"
        },
        "endpoints": [
            {
                "url": "/validate",
                "method": "POST",
                "description": "Validate JSON input"
            },
            {
                "url": "/docs",
                "method": "GET",
                "description": "API documentation"
            }
        ],
        "tags": ["json", "validator", "api"],
        "is_active": True,
        "stats": {
            "tests_passed": 42,
            "coverage": 0.95
        }
    })
    
    response = requests.post(
        f"{BASE_URL}/",
        data={"json_data": valid_json}
    )
    
    assert response.status_code == 200
    assert "✓ Valid JSON" in response.text
    assert "✗ Invalid JSON" not in response.text

def test_invalid_json():
    invalid_json = """
    {
        "project": "JSON Validator",
        "version": "1.0.0",
        "description": "A simple JSON validation service",
        "author": {
            "name": "Your Name",
            "email": "your.email@example.com"
        }
        "dependencies": {
            "python": ">=3.9",
            "docker": "latest"
        }
    }
    """
    
    response = requests.post(
        f"{BASE_URL}/",
        data={"json_data": invalid_json}
    )
    
    assert response.status_code == 200
    assert "✗ Invalid JSON" in response.text
    assert "✓ Valid JSON" not in response.text
    assert "Error:" in response.text