def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_task(client):
    response = client.post("/tasks", json={"title": "Test task"})
    assert response.status_code == 201
    assert response.json()["title"] == "Test task"

def test_list_tasks(client):
    client.post("/tasks", json={"title": "Task 1"})
    client.post("/tasks", json={"title": "Task 2"})
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_task(client):
    created = client.post("/tasks", json={"title": "My task"}).json()
    response = client.get(f"/tasks/{created['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "My task"

def test_get_task_not_found(client):
    response = client.get("/tasks/999")
    assert response.status_code == 404

def test_update_task(client):
    created = client.post("/tasks", json={"title": "Old title"}).json()
    response = client.put(f"/tasks/{created['id']}", json={"title": "New title"})
    assert response.status_code == 200
    assert response.json()["title"] == "New title"

def test_delete_task(client):
    created = client.post("/tasks", json={"title": "To delete"}).json()
    response = client.delete(f"/tasks/{created['id']}")
    assert response.status_code == 204
