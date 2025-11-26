from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory TODO list storage
todos = []
todo_id_counter = 1

@app.get("/")
def home():
    return jsonify({"message": "Python CI/CD Demo API with TODO List is running!"})

@app.get("/hello/<name>")
def greet(name):
    return jsonify({"greeting": f"Hello, {name}!"})

# Get all TODOs
@app.get("/todos")
def get_todos():
    return jsonify({"todos": todos})

# Get a specific TODO by ID
@app.get("/todos/<int:todo_id>")
def get_todo(todo_id):
    todo = next((t for t in todos if t["id"] == todo_id), None)
    if todo is None:
        return jsonify({"error": "TODO not found"}), 404
    return jsonify(todo)

# Create a new TODO
@app.post("/todos")
def create_todo():
    global todo_id_counter
    data = request.get_json()
    
    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400
    
    new_todo = {
        "id": todo_id_counter,
        "title": data["title"],
        "description": data.get("description", ""),
        "completed": False
    }
    todos.append(new_todo)
    todo_id_counter += 1
    
    return jsonify(new_todo), 201

# Update a TODO
@app.put("/todos/<int:todo_id>")
def update_todo(todo_id):
    todo = next((t for t in todos if t["id"] == todo_id), None)
    if todo is None:
        return jsonify({"error": "TODO not found"}), 404
    
    data = request.get_json()
    if "title" in data:
        todo["title"] = data["title"]
    if "description" in data:
        todo["description"] = data["description"]
    if "completed" in data:
        todo["completed"] = data["completed"]
    
    return jsonify(todo)

# Delete a TODO
@app.delete("/todos/<int:todo_id>")
def delete_todo(todo_id):
    global todos
    todo = next((t for t in todos if t["id"] == todo_id), None)
    if todo is None:
        return jsonify({"error": "TODO not found"}), 404
    
    todos = [t for t in todos if t["id"] != todo_id]
    return jsonify({"message": "TODO deleted successfully"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
