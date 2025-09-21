from fastapi.testclient import TestClient
from src.main import api, books

client = TestClient(api)

def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Welcome to the Book Management System"}

def test_add_book():
    response = client.post("/book", json={
        "id": 1,
        "name": "Book One",
        "description": "First test book",
        "isAvailable": True
    })
    assert response.status_code == 200
    assert any(book["id"] == 1 for book in response.json())

def test_get_books():
    response = client.get("/book")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1  # At least one book exists

def test_update_book():
    response = client.put("/book/1", json={
        "id": 1,
        "name": "Updated Book One",
        "description": "Updated description",
        "isAvailable": False
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Book One"
    assert data["isAvailable"] == False

def test_delete_book():
    response = client.delete("/book/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Updated Book One"

def test_delete_non_existing_book():
    response = client.delete("/book/99")
    assert response.status_code == 200
    assert response.json() == {"error": "Book not found, deletion failed"}