import logging
import os
import threading
from uuid import uuid4

from flask import Flask, jsonify, request, abort

from debug_decorator import auto_debug_with_openai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# In-memory data store for demonstration purposes
users = {}
users_lock = threading.Lock()


def _validated_name(data):
    name = data.get("name") if data else None
    if not isinstance(name, str) or not name.strip():
        abort(400, description="'name' must be a non-empty string")
    return name.strip()


@app.route("/users", methods=["POST"])
@auto_debug_with_openai
def create_user():
    """Create a new user with a unique ID."""
    name = _validated_name(request.get_json())

    user_id = str(uuid4())
    with users_lock:
        users[user_id] = {"id": user_id, "name": name}
    logger.info("Created user %s", user_id)
    return jsonify(users[user_id]), 201

@app.route("/users", methods=["GET"])
@auto_debug_with_openai
def get_users():
    """Retrieve all users."""
    with users_lock:
        return jsonify(list(users.values()))

@app.route("/users/<user_id>", methods=["GET"])
@auto_debug_with_openai
def get_user(user_id):
    """Retrieve a user by ID."""
    with users_lock:
        user = users.get(user_id)
        if not user:
            abort(404, description="User not found")
        return jsonify(user)

@app.route("/users/<user_id>", methods=["PUT"])
@auto_debug_with_openai
def update_user(user_id):
    """Update a user's name by ID."""
    name = _validated_name(request.get_json())

    with users_lock:
        user = users.get(user_id)
        if not user:
            abort(404, description="User not found")
        user["name"] = name
        logger.info("Updated user %s", user_id)
        return jsonify(user)

@app.route("/users/<user_id>", methods=["DELETE"])
@auto_debug_with_openai
def delete_user(user_id):
    """Delete a user by ID."""
    with users_lock:
        if user_id not in users:
            abort(404, description="User not found")
        deleted = users.pop(user_id)
    logger.info("Deleted user %s", user_id)
    return jsonify(deleted)

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
