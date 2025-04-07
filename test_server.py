import requests
import pytest
import json
import time
import socket
from threading import Thread
from server import run_server, PORT

BASE_URL = f"http://localhost:{PORT}"

def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

@pytest.fixture(scope="module")
def server():
    # Проверяем, занят ли порт
    if is_port_in_use(PORT):
        pytest.skip(f"Port {PORT} is already in use")

    # Запускаем сервер в отдельном потоке
    server_thread = Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Ждем, пока сервер не станет доступен
    for _ in range(10):
        try:
            requests.get(f"{BASE_URL}/", timeout=1)
            break
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            time.sleep(0.5)
    else:
        pytest.fail("Server did not start in time")
    
    yield
    
    # Сервер остановится автоматически, так как это демон-поток

def test_index_page(server):
    response = requests.get(f"{BASE_URL}/", timeout=5)
    assert response.status_code == 200
    assert "text/html" in response.headers["Content-Type"]

def test_static_files(server):
    content_types = {
        "style.css": "text/css",
        "script.js": "application/javascript"
    }
    
    for file, expected_type in content_types.items():
        response = requests.get(f"{BASE_URL}/static/{file}", timeout=5)
        assert response.status_code == 200
        assert expected_type in response.headers["Content-Type"]

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
        data={"json_data": valid_json},
        timeout=5
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
        data={"json_data": invalid_json},
        timeout=5
    )
    
    assert response.status_code == 200
    assert "✗ Invalid JSON" in response.text