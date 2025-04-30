# main.py
import os
from dotenv import load_dotenv
from flask import Flask

# Load environment variables from .env file
load_dotenv()

# Import the Flask app and decorator
from app import app


def start_server():
    """
    Starts the Flask server. Pulls host and port from environment variables if available.
    """
    host = os.getenv("FLASK_RUN_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_RUN_PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "true").lower() == "true"

    print(f"Starting server at http://{host}:{port} (debug={debug})")
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    start_server()

