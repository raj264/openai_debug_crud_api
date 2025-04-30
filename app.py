from flask import Flask, jsonify, request, abort
from uuid import uuid4
from debug_decorator import auto_debug_with_openai

app = Flask(__name__)

# In-memory data store for demonstration purposes
users = {}

@app.route("/users", methods=["POST"])
@auto_debug_with_openai
def create_user():
    """Create a new user with a unique ID."""
    data = request.get_json()
    if not data or not data.get("name"):
        abort(400, description="Missing 'name' in request body")

    user_id = str(uuid4())
    users[user_id] = {"id": user_id, "name": data["name"]}
    return jsonify(users[user_id]), 201

@app.route("/users", methods=["GET"])
@auto_debug_with_openai
def get_users():
    """Retrieve all users."""
    return jsonify(list(users.values()))

@app.route("/users/<user_id>", methods=["GET"])
@auto_debug_with_openai
def get_user(user_id):
    """Retrieve a user by ID."""
    user = users.get(user_id)
    if not user:
        abort(404, description="User not found")
    return jsonify(user)

@app.route("/users/<user_id>", methods=["PUT"])
@auto_debug_with_openai
def update_user(user_id):
    """Update a user's name by ID."""
    data = request.get_json()
    if not data or not data.get("name"):
        abort(400, description="Missing 'name' in request body")

    user = users.get(user_id)
    if not user:
        abort(404, description="User not found")

    user["name"] = data["name"]
    return jsonify(user)

@app.route("/users/<user_id>", methods=["DELETE"])
@auto_debug_with_openai
def delete_user(user_id):
    """Delete a user by ID."""
    if user_id not in users:
        abort(404, description="User not found")

    deleted = users.pop(user_id)
    return jsonify(deleted)

if __name__ == "__main__":
    app.run(debug=True)
