import requests
import pytest
import json
import time
import socket
from http.server import HTTPServer
from server import JSONValidatorHandler, PORT
from socket import socket

def find_free_port():
    with socket() as s:
        s.bind(('', 0))
        return s.getsockname()[1]

TEST_PORT = find_free_port()
PORT = TEST_PORT
BASE_URL = f"http://localhost:{PORT}"

@pytest.fixture(scope="module")
def server():
    # Создаем сервер, но пока не запускаем
    server = HTTPServer(('localhost', PORT), JSONValidatorHandler)
    
    # Запускаем в отдельном потоке
    import threading
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    # Даем серверу время на запуск
    time.sleep(1)
    
    yield server
    
    # Останавливаем сервер после тестов
    server.shutdown()
    server.server_close()
    server_thread.join()

def is_server_running():
    try:
        return requests.get(f"{BASE_URL}/", timeout=1).status_code == 200
    except:
        return False

def test_index_page(server):
    assert is_server_running(), "Server is not running"
    response = requests.get(f"{BASE_URL}/", timeout=5)
    assert response.status_code == 200
    assert "text/html" in response.headers["Content-Type"]

def test_static_files(server):
    assert is_server_running(), "Server is not running"
    content_types = {
        "style.css": "text/css",
        "script.js": "application/javascript"
    }
    
    for file, expected_type in content_types.items():
        response = requests.get(f"{BASE_URL}/static/{file}", timeout=5)
        assert response.status_code == 200
        assert expected_type in response.headers["Content-Type"]

def test_valid_json(server):
    assert is_server_running(), "Server is not running"
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
    assert is_server_running(), "Server is not running"
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