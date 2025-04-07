import requests
import pytest

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