import requests
import pytest
import json
import time
from threading import Thread
from server import run_server, PORT

BASE_URL = f"http://localhost:{PORT}"

@pytest.fixture(scope="module")
def server():
    # Запускаем сервер в отдельном потоке
    server_thread = Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Даем серверу время на запуск
    time.sleep(2)
    
    yield  # здесь выполняются тесты
    
    # По завершении тестов сервер будет остановлен автоматически,
    # так как это демон-поток

def test_index_page(server):
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    assert "text/html" in response.headers["Content-Type"]

def test_static_files(server):
    for file in ["style.css", "script.js"]:
        response = requests.get(f"{BASE_URL}/static/{file}")
        assert response.status_code == 200
        assert file.split(".")[-1] in response.headers["Content-Type"]

def test_valid_json(server):
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

def test_invalid_json(server):
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