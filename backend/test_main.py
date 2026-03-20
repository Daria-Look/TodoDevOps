from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# --- Тестируется создание задачи (POST) --- 
def test_create_todo():
    response = client.post("/items", json={"title": "Test Task"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["completed"] is False
    assert "id" in data

# --- Тестируется получение списка (GET) --- 
def test_read_todos():
    # --- Сначала создание, чтобы список не был пустым --- 
    client.post("/items", json={"title": "Another Task"})
    
    response = client.get("/items")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any(item["title"] == "Another Task" for item in data)

# --- Тестируется удаление (DELETE) --- 
def test_delete_todo():
    # --- Создание задачи, чтобы её удалить --- 
    create_res = client.post("/items", json={"title": "Delete Me"})
    todo_id = create_res.json()["id"]
    
    response = client.delete(f"/items/{todo_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Deleted"}