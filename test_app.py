from app import app

def test_home():
    client = app.test_client()
    res = client.get("/")
    assert res.status_code == 200
    assert res.json["message"] == "Python CI/CD Demo API with TODO List is running!"

def test_greet():
    client = app.test_client()
    res = client.get("/hello/Pratham")
    assert res.status_code == 200
    assert res.json["greeting"] == "Hello, Pratham!"  # Matches requested name

# TODO List Test Cases

def test_get_todos_empty():
    """Test retrieving TODOs when list is empty"""
    client = app.test_client()
    res = client.get("/todos")
    assert res.status_code == 200
    # Accept either empty list or only seeded data, but assert type
    assert isinstance(res.json["todos"], list)

def test_create_todo():
    """Test creating a new TODO"""
    client = app.test_client()
    res = client.post("/todos", json={
        "title": "Buy groceries",
        "description": "Buy milk, eggs, and bread"
    })
    assert res.status_code == 201
    assert res.json["title"] == "Buy groceries"
    assert res.json["description"] == "Buy milk, eggs, and bread"
    assert res.json["completed"] is False
    assert "id" in res.json

def test_create_todo_missing_title():
    """Test creating TODO without title (should fail)"""
    client = app.test_client()
    res = client.post("/todos", json={"description": "Some task"})
    assert res.status_code == 400
    assert "error" in res.json

def test_create_todo_empty_body():
    """Test creating TODO with empty request body (should fail)"""
    client = app.test_client()
    res = client.post("/todos", json={})
    assert res.status_code == 400
    assert "error" in res.json

def test_get_all_todos():
    """Test retrieving all TODOs after creating some"""
    client = app.test_client()
    # Create expected TODOs
    client.post("/todos", json={"title": "Task 1", "description": "First task"})
    client.post("/todos", json={"title": "Task 2"})
    # Get all TODOs
    res = client.get("/todos")
    assert res.status_code == 200
    titles = [todo["title"] for todo in res.json["todos"]]
    assert "Task 1" in titles
    assert "Task 2" in titles

def test_get_todo_by_id():
    """Test retrieving a specific TODO by ID"""
    client = app.test_client()
    create_res = client.post("/todos", json={"title": "Test TODO"})
    todo_id = create_res.json["id"]
    res = client.get(f"/todos/{todo_id}")
    assert res.status_code == 200
    assert res.json["title"] == "Test TODO"
    assert res.json["id"] == todo_id

def test_get_todo_not_found():
    """Test retrieving a TODO that doesn't exist"""
    client = app.test_client()
    res = client.get("/todos/9999")
    assert res.status_code == 404
    assert "error" in res.json

def test_update_todo_title():
    """Test updating TODO title"""
    client = app.test_client()
    create_res = client.post("/todos", json={"title": "Old title"})
    todo_id = create_res.json["id"]
    res = client.put(f"/todos/{todo_id}", json={"title": "New title"})
    assert res.status_code == 200
    assert res.json["title"] == "New title"

def test_update_todo_completion_status():
    """Test updating TODO completion status"""
    client = app.test_client()
    create_res = client.post("/todos", json={"title": "Complete this"})
    todo_id = create_res.json["id"]
    res = client.put(f"/todos/{todo_id}", json={"completed": True})
    assert res.status_code == 200
    assert res.json["completed"] is True

def test_update_todo_description():
    """Test updating TODO description"""
    client = app.test_client()
    create_res = client.post("/todos", json={"title": "Task", "description": "Old description"})
    todo_id = create_res.json["id"]
    res = client.put(f"/todos/{todo_id}", json={"description": "New description"})
    assert res.status_code == 200
    assert res.json["description"] == "New description"

def test_update_todo_not_found():
    """Test updating a TODO that doesn't exist"""
    client = app.test_client()
    res = client.put("/todos/9999", json={"title": "New title"})
    assert res.status_code == 404
    assert "error" in res.json

def test_delete_todo():
    """Test deleting a TODO"""
    client = app.test_client()
    create_res = client.post("/todos", json={"title": "Delete me"})
    todo_id = create_res.json["id"]
    res = client.delete(f"/todos/{todo_id}")
    assert res.status_code == 200
    assert "message" in res.json
    get_res = client.get(f"/todos/{todo_id}")
    assert get_res.status_code == 404

def test_delete_todo_not_found():
    """Test deleting a TODO that doesn't exist"""
    client = app.test_client()
    res = client.delete("/todos/9999")
    assert res.status_code == 404
    assert "error" in res.json

def test_create_todo_with_only_title():
    """Test creating TODO with only title (description optional)"""
    client = app.test_client()
    res = client.post("/todos", json={"title": "Only title"})
    assert res.status_code == 201
    assert res.json["title"] == "Only title"
    # Accept empty description or default
    assert res.json.get("description", "") in ("", None)
    assert res.json["completed"] is False
